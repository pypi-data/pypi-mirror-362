import docker
import os
import hashlib
from pathlib import Path
from rich.console import Console
import click
import importlib.metadata

console = Console()

class CDockManager:
    def __init__(self):
        self.client = docker.from_env()
        self.docker_image = "claude-code"
        self.default_ssh_key = Path.home() / ".ssh" / "cdock"

    def check_dangerous_directory(self):
        """Check if running in sensitive directory"""
        current_dir = Path.cwd()
        dangerous_dirs = [Path.home(), Path("/"), Path("/root")]

        if current_dir in dangerous_dirs:
            console.print(f"[yellow]⚠️  Running cdock in sensitive directory: {current_dir}[/yellow]")
            console.print("This could give Claude access to your entire system.")
            if not click.confirm("Continue?"):
                raise click.Abort()

    def get_volume_name(self):
        """Generate unique volume name for current directory"""
        full_path = Path.cwd().resolve()
        path_hash = hashlib.sha256(str(full_path).encode()).hexdigest()[:8]
        repo_name = full_path.name
        return f"cdock-{repo_name}-{path_hash}"

    def _get_ssh_mounts(self):
        """Get SSH key mount configuration"""
        ssh_mounts = {}
        ssh_key = Path(os.getenv("CDOCK_SSH_KEY", self.default_ssh_key))
        
        if ssh_key.exists():
            ssh_mounts[str(ssh_key)] = {
                "bind": "/root/.ssh/id_rsa",
                "mode": "ro"
            }
            
            pub_key = ssh_key.with_suffix(".pub")
            if pub_key.exists():
                ssh_mounts[str(pub_key)] = {
                    "bind": "/root/.ssh/id_rsa.pub", 
                    "mode": "ro"
                }
        else:
            console.print(f"[yellow]⚠️  SSH key not found at {ssh_key}[/yellow]")
            console.print("SSH operations may fail. Create key or set CDOCK_SSH_KEY")
        
        return ssh_mounts

    def run_container(self, args):
        """Run Docker container with current directory mounted"""
        self.check_dangerous_directory()
        
        # Get volume and directory info
        vol_name = self.get_volume_name()
        current_dir = Path.cwd()
        username = os.getenv("USER", "user")
        
        # SSH key handling
        ssh_mounts = self._get_ssh_mounts()
        
        # Build volume mounts
        volumes = {
            str(current_dir): {"bind": f"/home/{username}/git/{current_dir.name}", "mode": "rw"},
            vol_name: {"bind": f"/home/{username}/git/{current_dir.name}/.venv", "mode": "rw"},
            "uv-global-cache": {"bind": f"/home/{username}/.cache/uv", "mode": "rw"},
            "claude-home-auth": {"bind": f"/home/{username}/.claude-auth", "mode": "rw"},
            **ssh_mounts
        }
        
        # Add Claude config mounts if they exist
        claude_dir = Path.home() / ".claude"
        claude_file = Path.home() / ".claude.json"
        
        if claude_dir.exists():
            volumes[str(claude_dir)] = {"bind": "/host-claude-dir", "mode": "ro"}
        if claude_file.exists():
            volumes[str(claude_file)] = {"bind": "/host-claude-file", "mode": "ro"}
        
        # Environment variables
        environment = {
            "HOST_UID": str(os.getuid()),
            "HOST_GID": str(os.getgid()),
            "HOST_USERNAME": username,
            "UV_LINK_MODE": "copy"
        }
        
        # Check if we have a TTY for interactive vs non-interactive mode
        has_tty = os.isatty(0) and os.isatty(1)
        
        # Container configuration
        container_config = {
            "image": self.docker_image,
            "command": args or None,
            "volumes": volumes,
            "environment": environment,
            "remove": True,
            "detach": not has_tty,  # Detach when no TTY (non-interactive)
            "stdin_open": has_tty,
            "tty": has_tty
        }
        
        try:
            console.print(f"[green]Running container with image: {self.docker_image}[/green]")
            result = self.client.containers.run(**container_config)
            
            if has_tty:
                # Interactive mode - result is container output
                return result
            else:
                # Non-interactive mode - result is container object, return immediately
                console.print(f"[blue]Container {result.id[:12]} started in background[/blue]")
                return result
        except docker.errors.ImageNotFound:
            console.print(f"[red]Docker image '{self.docker_image}' not found[/red]")
            console.print("Run 'cdock upgrade' to build the image")
            raise click.Abort()
        except docker.errors.DockerException as e:
            console.print(f"[red]Docker error: {e}[/red]")
            raise click.Abort()
        except Exception as e:
            console.print(f"[red]Error running container: {e}[/red]")
            raise click.Abort()

    def _get_containers_using_volume(self, volume_name):
        """Get containers that are using a specific volume"""
        containers = []
        try:
            for container in self.client.containers.list(all=True):
                if container.attrs.get('Mounts'):
                    for mount in container.attrs['Mounts']:
                        if mount.get('Name') == volume_name:
                            containers.append(container)
                            break
        except docker.errors.DockerException:
            pass
        return containers

    def needs_upgrade(self):
        """Check if Docker image needs upgrade based on version"""
        try:
            # Get current package version
            package_version = importlib.metadata.version('cdock')
            
            # Get image and check label
            image = self.client.images.get(self.docker_image)
            image_version = image.labels.get('cdock.version')
            
            if image_version != package_version:
                console.print(f"[yellow]Image version {image_version or 'unknown'} != package version {package_version}[/yellow]")
                return True
            
            console.print(f"[green]Image version {image_version} matches package version[/green]")
            return False
            
        except docker.errors.ImageNotFound:
            console.print(f"[yellow]Image {self.docker_image} not found[/yellow]")
            return True
        except Exception as e:
            console.print(f"[yellow]Cannot check version: {e}[/yellow]")
            return True

    def clean_volumes(self, all_volumes=False, force=False):
        """Clean volumes"""
        if all_volumes:
            console.print("[yellow]Cleaning all cdock volumes system-wide...[/yellow]")
            try:
                # Get all volumes that match cdock patterns
                volumes = self.client.volumes.list()
                cdock_volumes = [v for v in volumes if v.name.startswith("claude-venv-") or v.name.startswith("cdock-")]
                
                # Also clean global volumes
                global_volumes = ["uv-global-cache", "claude-home-auth"]
                
                removed_count = 0
                for volume in cdock_volumes:
                    try:
                        volume.remove()
                        console.print(f"[green]Removed volume: {volume.name}[/green]")
                        removed_count += 1
                    except docker.errors.APIError as e:
                        if "volume is in use" in str(e):
                            containers = self._get_containers_using_volume(volume.name)
                            if force and containers:
                                console.print(f"[yellow]Force stopping and removing containers using {volume.name}[/yellow]")
                                for container in containers:
                                    container.stop()
                                    container.remove()
                                    console.print(f"[yellow]Stopped and removed container: {container.name or container.id[:12]}[/yellow]")
                                try:
                                    volume.remove()
                                    console.print(f"[green]Removed volume: {volume.name}[/green]")
                                    removed_count += 1
                                except docker.errors.APIError as e2:
                                    console.print(f"[red]Still couldn't remove {volume.name}: {e2}[/red]")
                            else:
                                console.print(f"[yellow]Volume {volume.name} is in use by containers:[/yellow]")
                                for container in containers:
                                    status = container.status
                                    name = container.name or container.id[:12]
                                    console.print(f"  - {name} ({status})")
                                console.print(f"[blue]Use --force to stop containers and remove volume[/blue]")
                        else:
                            console.print(f"[red]Error removing {volume.name}: {e}[/red]")
                
                # Clean global volumes
                for vol_name in global_volumes:
                    try:
                        volume = self.client.volumes.get(vol_name)
                        volume.remove()
                        console.print(f"[green]Removed global volume: {vol_name}[/green]")
                        removed_count += 1
                    except docker.errors.NotFound:
                        pass  # Volume doesn't exist
                    except docker.errors.APIError as e:
                        if "volume is in use" in str(e):
                            console.print(f"[yellow]Skipping global volume in use: {vol_name}[/yellow]")
                        else:
                            console.print(f"[red]Error removing {vol_name}: {e}[/red]")
                
                console.print(f"[green]✅ Cleaned {removed_count} volumes system-wide[/green]")
                
            except docker.errors.DockerException as e:
                console.print(f"[red]Docker error: {e}[/red]")
                raise click.Abort()
        else:
            console.print("[yellow]Cleaning local project volumes...[/yellow]")
            vol_name = self.get_volume_name()
            
            try:
                volume = self.client.volumes.get(vol_name)
                volume.remove()
                console.print(f"[green]✅ Removed project volume: {vol_name}[/green]")
            except docker.errors.NotFound:
                console.print(f"[yellow]Volume {vol_name} not found[/yellow]")
            except docker.errors.APIError as e:
                if "volume is in use" in str(e):
                    containers = self._get_containers_using_volume(vol_name)
                    if force and containers:
                        console.print(f"[yellow]Force stopping and removing containers using {vol_name}[/yellow]")
                        for container in containers:
                            container.stop()
                            container.remove()
                            console.print(f"[yellow]Stopped and removed container: {container.name or container.id[:12]}[/yellow]")
                        try:
                            volume.remove()
                            console.print(f"[green]✅ Removed project volume: {vol_name}[/green]")
                        except docker.errors.APIError as e2:
                            console.print(f"[red]Still couldn't remove {vol_name}: {e2}[/red]")
                            raise click.Abort()
                    else:
                        console.print(f"[yellow]Volume {vol_name} is in use by containers:[/yellow]")
                        for container in containers:
                            status = container.status
                            name = container.name or container.id[:12]
                            console.print(f"  - {name} ({status})")
                        console.print(f"[blue]Use --force to stop containers and remove volume[/blue]")
                else:
                    console.print(f"[red]Error removing volume: {e}[/red]")
                    raise click.Abort()

    def upgrade(self, force_rebuild=False):
        """Rebuild Docker image with optional cache"""
        # Check if upgrade is needed (unless forced)
        if not force_rebuild and not self.needs_upgrade():
            console.print("[green]✅ Image is up to date, no upgrade needed[/green]")
            return
        
        if force_rebuild:
            console.print("[blue]Forcing complete image rebuild...[/blue]")
            # Remove existing image if it exists
            try:
                self.client.images.remove(self.docker_image, force=True)
                console.print(f"[yellow]Removed existing image: {self.docker_image}[/yellow]")
            except docker.errors.ImageNotFound:
                console.print(f"[yellow]Image {self.docker_image} not found, will build new[/yellow]")
            except docker.errors.APIError as e:
                console.print(f"[yellow]Warning: {e}[/yellow]")
        else:
            console.print("[blue]Rebuilding image (using cache)...[/blue]")
        
        # Build new image from current directory or extract from package
        dockerfile_path = Path.cwd() / "Dockerfile"
        build_path = Path.cwd()
        
        if not dockerfile_path.exists():
            # Extract Dockerfile and entrypoint.sh from package
            import tempfile
            import shutil
            try:
                import importlib.resources as pkg_resources
            except ImportError:
                import importlib_resources as pkg_resources
            
            console.print("[blue]Extracting Dockerfile from package...[/blue]")
            
            temp_dir = Path(tempfile.mkdtemp())
            try:
                # Extract Dockerfile
                with pkg_resources.files('cdock').joinpath('Dockerfile').open('r') as f:
                    dockerfile_content = f.read()
                dockerfile_path = temp_dir / "Dockerfile"
                dockerfile_path.write_text(dockerfile_content)
                
                # Extract entrypoint.sh
                with pkg_resources.files('cdock').joinpath('entrypoint.sh').open('r') as f:
                    entrypoint_content = f.read()
                entrypoint_path = temp_dir / "entrypoint.sh"
                entrypoint_path.write_text(entrypoint_content)
                entrypoint_path.chmod(0o755)
                
                build_path = temp_dir
                console.print(f"[green]Extracted build files to {temp_dir}[/green]")
                
            except Exception as e:
                console.print(f"[red]Failed to extract build files: {e}[/red]")
                console.print("Run 'cdock upgrade' from the cdock repository root")
                raise click.Abort()
        
        try:
            console.print(f"[blue]Building image: {self.docker_image}[/blue]")
            
            # Get package version for build arg
            package_version = importlib.metadata.version('cdock')
            
            # Use low-level API for streaming build output
            import sys
            import json
            
            response = self.client.api.build(
                path=str(build_path),
                tag=self.docker_image,
                rm=True,
                forcerm=force_rebuild,
                nocache=force_rebuild,
                buildargs={'CDOCK_VERSION': package_version},
                decode=True
            )
            
            # Stream build output in real-time
            for log in response:
                if 'stream' in log:
                    output = log['stream'].strip()
                    if output:
                        print(output)
                        sys.stdout.flush()
                elif 'error' in log:
                    console.print(f"[red]Build error: {log['error']}[/red]")
                    raise docker.errors.BuildError(log['error'], response)
            
            console.print(f"[green]✅ Successfully built image: {self.docker_image}[/green]")
            
        except docker.errors.BuildError as e:
            console.print(f"[red]Build failed: {e}[/red]")
            raise click.Abort()
        except docker.errors.APIError as e:
            console.print(f"[red]Docker API error: {e}[/red]")
            raise click.Abort()
        finally:
            # Clean up temp directory if we created one
            if build_path != Path.cwd():
                import shutil
                shutil.rmtree(build_path, ignore_errors=True)