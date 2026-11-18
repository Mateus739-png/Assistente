import subprocess
import tempfile
import os


POWERSHELL = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"


def controlar_bluetooth(estado):
    script = f"""
If ((Get-Service bthserv).Status -eq 'Stopped') {{
    Start-Service bthserv
}}

Add-Type -AssemblyName System.Runtime.WindowsRuntime

[Windows.Devices.Radios.Radio,Windows.System.Devices,ContentType=WindowsRuntime] | Out-Null
[Windows.Devices.Radios.RadioAccessStatus,Windows.System.Devices,ContentType=WindowsRuntime] | Out-Null
[Windows.Devices.Radios.RadioState,Windows.System.Devices,ContentType=WindowsRuntime] | Out-Null

$asTaskGeneric = ([System.WindowsRuntimeSystemExtensions].GetMethods() |
    Where-Object {{
        $_.Name -eq 'AsTask' -and
        $_.GetParameters().Count -eq 1 -and
        $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1'
    }})[0]

function Await($WinRtTask, $ResultType) {{
    $asTask = $asTaskGeneric.MakeGenericMethod($ResultType)
    $netTask = $asTask.Invoke($null, @($WinRtTask))
    $netTask.Wait(-1) | Out-Null
    $netTask.Result
}}

$access = Await `
    ([Windows.Devices.Radios.Radio]::RequestAccessAsync()) `
    ([Windows.Devices.Radios.RadioAccessStatus])

if ($access.ToString() -ne "Allowed") {{
    Write-Error "Acesso ao Bluetooth negado: $access"
    exit 1
}}

$radios = Await `
    ([Windows.Devices.Radios.Radio]::GetRadiosAsync()) `
    ([System.Collections.Generic.IReadOnlyList[Windows.Devices.Radios.Radio]])

$bluetooth = $radios |
    Where-Object {{ $_.Kind -eq 'Bluetooth' }} |
    Select-Object -First 1

if ($null -eq $bluetooth) {{
    Write-Error "Bluetooth não encontrado."
    exit 1
}}

$status = Await `
    ($bluetooth.SetStateAsync([Windows.Devices.Radios.RadioState]::{estado})) `
    ([Windows.Devices.Radios.RadioAccessStatus])

if ($status.ToString() -ne "Allowed") {{
    Write-Error "Não foi possível alterar o Bluetooth: $status"
    exit 1
}}

Start-Sleep -Milliseconds 500

$radios2 = Await `
    ([Windows.Devices.Radios.Radio]::GetRadiosAsync()) `
    ([System.Collections.Generic.IReadOnlyList[Windows.Devices.Radios.Radio]])

$bluetooth2 = $radios2 |
    Where-Object {{ $_.Kind -eq 'Bluetooth' }} |
    Select-Object -First 1

Write-Output ("ESTADO=" + $bluetooth2.State)
"""

    arquivo_temp = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".ps1",
            delete=False,
            encoding="utf-8"
        ) as arquivo:
            arquivo.write(script)
            arquivo_temp = arquivo.name

        resultado = subprocess.run(
            [
                POWERSHELL,
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                arquivo_temp
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        if resultado.returncode != 0:
            erro = resultado.stderr.strip()

            if erro:
                print("⚠️ Bluetooth:", erro)

            return "Não consegui alterar o Bluetooth."

        return (
            "Bluetooth ligado."
            if estado == "On"
            else "Bluetooth desligado."
        )

    finally:
        if arquivo_temp and os.path.exists(arquivo_temp):
            try:
                os.remove(arquivo_temp)
            except OSError:
                pass


def ligar_bluetooth():
    return controlar_bluetooth("On")


def desligar_bluetooth():
    return controlar_bluetooth("Off")

# Compatibilidade com o __init__.py antigo
bluetooth_ligar = ligar_bluetooth
bluetooth_desligar = desligar_bluetooth