# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Configura o executável principal
a = Analysis(
    ['main.py'],  # O arquivo principal da sua aplicação
    pathex=['D:/PycharmProjects/BemBanhado_petshop/CadastroClientes'],  # Caminho do diretório do projeto
    binaries=[],
    datas=[('ui/main_window.ui', 'ui'),  # Adiciona o arquivo de interface
           ('LogoBBx.png', '.')],  # Adiciona a logo
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Opções de empacotamento
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Gera o executável
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PetBook',  # Nome do executável
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # False para aplicações GUI
    icon='LogoPetBook.ico'  # Caminho do ícone do executável
)

# Configuração para o diretório dist com arquivos necessários
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PetBook'
)
