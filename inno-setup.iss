#define MyAppName "Mosque Management System"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Salman Asmat"
#define MyAppExeName "MosqueManagementSystem.exe"
#define MyAppDir "Mosque Management System"

[Setup]
AppId=MosqueManagementSystem
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppDir}
DefaultGroupName={#MyAppName}
OutputDir=.\installer-output
OutputBaseFilename=MosqueManagementSystem-Setup
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayIcon={app}\{#MyAppExeName}

[Files]
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "mosque.db"; DestDir: "{app}"; Flags: onlyifdoesntexist uninsneveruninstall

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"

[UninstallDelete]
Type: files; Name: "{app}\{#MyAppExeName}"
