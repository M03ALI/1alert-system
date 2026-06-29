; Inno Setup script — wraps the built program into a real Windows installer.
; Produces  installer_output\StockInventory-Setup.exe  (Start Menu + Desktop
; shortcuts and an uninstaller). The user's code is compiled inside the program,
; not shipped as readable source.

[Setup]
AppName=Stock Inventory
AppVersion=1.1.0
AppPublisher=Health Data Matrics
DefaultDirName={autopf}\StockInventory
DefaultGroupName=Stock Inventory
DisableProgramGroupPage=yes
OutputDir=installer_output
OutputBaseFilename=StockInventory-Setup
SetupIconFile=logo.ico
UninstallDisplayIcon={app}\StockInventory.exe
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"

[Files]
; Bundle the entire built program folder (produced by PyInstaller).
Source: "dist\StockInventory\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion

[Icons]
Name: "{group}\Stock Inventory"; Filename: "{app}\StockInventory.exe"; IconFilename: "{app}\logo.ico"
Name: "{group}\Uninstall Stock Inventory"; Filename: "{uninstallexe}"
Name: "{commondesktop}\Stock Inventory"; Filename: "{app}\StockInventory.exe"; IconFilename: "{app}\logo.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\StockInventory.exe"; Description: "Launch Stock Inventory now"; Flags: nowait postinstall skipifsilent
