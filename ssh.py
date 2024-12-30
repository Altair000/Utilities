import os
import subprocess
import socket
import platform
import distro
import urllib.request

def install_ssh_server():
    os_type = platform.system().lower()

    if os_type == 'linux':
        # Obtener la distribución de Linux con 'distro'
        distro_name = distro.id().lower()
        print(f"Distribución de Linux detectada: {distro_name}")
        
        if 'ubuntu' in distro_name or 'debian' in distro_name:
            subprocess.run(["sudo", "apt", "update"], check=True)
            subprocess.run(["sudo", "apt", "install", "-y", "openssh-server"], check=True)
        elif 'centos' in distro_name or 'rhel' in distro_name:
            subprocess.run(["sudo", "yum", "install", "-y", "openssh-server"], check=True)
        elif 'fedora' in distro_name:
            subprocess.run(["sudo", "dnf", "install", "-y", "openssh-server"], check=True)
        else:
            print("Distribución no soportada para instalación automática de SSH.")
            return
        print("OpenSSH instalado correctamente en Linux.")

    elif os_type == 'windows':
        arch = platform.architecture()[0]
        print(f"Arquitectura de Windows detectada: {arch}")

        # Windows no tiene OpenSSH instalado por defecto en versiones anteriores
        if arch == '64bit':
            print("Instalando OpenSSH para Windows de 64 bits.")
            subprocess.run(['powershell', 'Add-WindowsFeature', 'OpenSSH.Server'], check=True)
        elif arch == '32bit':
            print("Instalando OpenSSH para Windows de 32 bits.")
            subprocess.run(['powershell', 'Add-WindowsFeature', 'OpenSSH.Server'], check=True)
        else:
            print("Arquitectura no soportada.")
            return
        print("OpenSSH instalado correctamente en Windows.")
    else:
        print("Sistema operativo no soportado.")
        return

def start_ssh_service():
    # Inicia y habilita el servicio SSH en Linux o Windows
    os_type = platform.system().lower()

    if os_type == 'linux':
        subprocess.run(["sudo", "systemctl", "start", "sshd"], check=True)
        subprocess.run(["sudo", "systemctl", "enable", "sshd"], check=True)
        print("Servicio SSH iniciado y habilitado en Linux.")
    elif os_type == 'windows':
        subprocess.run(['powershell', 'Start-Service', 'sshd'], check=True)
        subprocess.run(['powershell', 'Set-Service', 'sshd', '-StartupType', 'Automatic'], check=True)
        print("Servicio SSH iniciado y habilitado en Windows.")
    else:
        print("Sistema operativo no soportado para iniciar el servicio SSH.")
        return

def get_ip_address():
    # Obtener la IP local
    local_ip = socket.gethostbyname(socket.gethostname())

    # Obtener la IP pública usando un servicio externo
    try:
        public_ip = urllib.request.urlopen('https://api.ipify.org').read().decode('utf8')
    except Exception as e:
        public_ip = "No se pudo obtener la IP pública."

    return local_ip, public_ip

def configure_ssh():
    config_file = "/etc/ssh/sshd_config" if platform.system().lower() == "linux" else "C:\\ProgramData\\ssh\\sshd_config"
    
    try:
        with open(config_file, "r") as file:
            config = file.read()

        # Verificar y modificar la configuración necesaria para SSH
        # Habilitar PasswordAuthentication
        if "PasswordAuthentication yes" not in config:
            config = config.replace("#PasswordAuthentication yes", "PasswordAuthentication yes") if "#PasswordAuthentication yes" in config else config
            with open(config_file, "a") as file:
                file.write("\nPasswordAuthentication yes\n")
            print("Autenticación por contraseña habilitada.")
        
        # Habilitar otras configuraciones necesarias, como permitir el acceso root si es necesario
        if "PermitRootLogin yes" not in config:
            config = config.replace("#PermitRootLogin yes", "PermitRootLogin yes") if "#PermitRootLogin yes" in config else config
            with open(config_file, "a") as file:
                file.write("\nPermitRootLogin yes\n")
            print("Acceso root habilitado.")
        # Reiniciar el servicio SSH para aplicar cambios
        if platform.system().lower() == "linux":
            subprocess.run(["sudo", "systemctl", "restart", "sshd"], check=True)
            print("Configuración de SSH aplicada en Linux y servicio reiniciado.")
        elif platform.system().lower() == "windows":
            subprocess.run(['powershell', 'Restart-Service', 'sshd'], check=True)
            print("Configuración de SSH aplicada en Windows y servicio reiniciado.")
        
    except Exception as e:
        print(f"Error al configurar SSH: {e}")

def print_credentials(local_ip, public_ip):
    print("\n--- Credenciales de SSH ---")
    print(f"IP Local del servidor: {local_ip}")
    print(f"IP Pública del servidor: {public_ip}")
    print("Usuario: root (o el nombre de usuario configurado)")
    print("Contraseña: (la que hayas configurado en el servidor)")
    print("Para conectarte desde otro ordenador usa el siguiente comando SSH:")
    print(f"ssh root@{local_ip}")
    print("\n--- Fin de las credenciales ---")

def main():
    install_ssh_server()
    start_ssh_service()
    configure_ssh()

    local_ip, public_ip = get_ip_address()
    print_credentials(local_ip, public_ip)

if __name__ == "__main__":
    main()
