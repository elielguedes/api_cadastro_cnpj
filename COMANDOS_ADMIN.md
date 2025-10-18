# 🎉 COMANDOS PARA COPIAR NO POWERSHELL ADMIN

## ✅ WSL JÁ INSTALADO! Agora execute no PowerShell Admin:

```powershell
# Navegar para o projeto
cd C:\Users\eliel\.vscode\framework_udf

# 1. Habilitar Plataforma VM
Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform -All -NoRestart

# 2. Baixar kernel WSL2
Invoke-WebRequest -Uri "https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi" -OutFile "wsl_update_x64.msi"

# 3. Instalar kernel (aguardar terminar)
Start-Process msiexec.exe -Wait -ArgumentList '/i wsl_update_x64.msi /quiet'

# 4. Configurar WSL2
wsl --set-default-version 2

# 5. Verificar
wsl --version

# 6. Reiniciar Docker Desktop
Stop-Process -Name "Docker Desktop" -ErrorAction SilentlyContinue
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"

# 7. Aguardar e testar (após 30 segundos)
Start-Sleep 30
docker --version
docker info
```

## 🚀 DEPOIS DE EXECUTAR TUDO:
Volte para o VS Code e execute:
```powershell
.\docker-manage.ps1 check
```

## 🎯 SE TUDO FUNCIONAR:
```powershell
# Testar Docker Compose
docker-compose config

# Rodar apenas PostgreSQL
.\docker-manage.ps1 db-only

# Ou aplicação completa
.\docker-manage.ps1 up
```