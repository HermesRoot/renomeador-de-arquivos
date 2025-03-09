# Renomeador de Arquivos 

Este é um renomeador de arquivos simples, mas poderoso, desenvolvido em Python utilizando a biblioteca wxPython para uma interface gráfica de fácil uso. O programa permite renomear múltiplos arquivos de forma rápida, aplicando prefixos e números sequenciais personalizados. Ele também oferece a funcionalidade de desfazer as renomeações realizadas, salvando logs detalhados das alterações feitas.

## 🖥️ Captura de Tela
![Screenshot do renomeador-de-arquivos](https://raw.githubusercontent.com/HermesRoot/renomeador-de-arquivos/refs/heads/main/screenshot.jpg)

## 🛠️ Funcionalidades 

- **Seleção de Arquivos**: Permite a seleção de múltiplos arquivos de diferentes formatos, como `.mp4`, `.jpg`, `.txt`, etc.
- **Configurações de Renomeação**:
  - Defina um prefixo para os arquivos renomeados.
  - Personalize o número inicial e o separador entre o prefixo e o contador.
  - Visualize a prévia dos novos nomes dos arquivos antes de confirmar a renomeação.
- **Desfazer Renomeações**: Caso necessário, é possível desfazer as alterações de renomeação.
- **Salvar Log de Renomeações**: O programa gera um log com os detalhes das renomeações feitas.
- **Definir Extensões Personalizadas**: Permite alterar as extensões de arquivo suportadas para renomeação.
- **Interface Gráfica**: A interface gráfica é feita com wxPython, facilitando o uso e a visualização dos arquivos.

## 🚀 Como Usar 

1. **Abrir o Programa**: Ao iniciar o programa, você verá a interface gráfica.
2. **Selecionar Arquivos**: Clique no botão "..." para escolher os arquivos que você deseja renomear. Você pode selecionar vários arquivos de uma vez.
3. **Definir Configurações**: 
   - Digite o **prefixo** que deseja usar nos nomes dos arquivos.
   - Defina o **número inicial** e o **separador** (se houver) para os arquivos renomeados.
4. **Visualizar Prévia**: Após configurar as opções, uma prévia do novo nome dos arquivos será exibida.
5. **Renomear**: Clique no botão "Renomear" para aplicar as alterações.
6. **Desfazer**: Caso necessário, clique em "Desfazer" para reverter as renomeações realizadas.
7. **Salvar Log**: Após renomear os arquivos, você pode salvar um log com todas as alterações feitas.
8. **Gerenciar Extensões**: Através do menu "Editar", você pode personalizar as extensões de arquivos que o programa reconhece.

## 🗂️ Extensões Suportadas

Por padrão, o programa suporta as seguintes extensões:

- Vídeos: `.mp4`, `.mkv`, `.avi`, `.mov`, `.wmv`, `.flv`
- Áudio: `.mp3`, `.wav`, `.ogg`
- Imagens: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`
- Documentos: `.txt`, `.pdf`, `.docx`, `.xlsx`

Você pode editar a lista de extensões suportadas no menu "Editar" > "Definir Extensões Personalizadas".

## 📋 Pré-requisitos

- Python 3.x
- wxPython (versão 4.1 ou superior)

### Instalando o wxPython

Se você não tiver o wxPython instalado, pode instalá-lo com o seguinte comando:

```bash
pip install wxPython
```

## 🚀 Como Executar

- Clone o repositório ou faça o download dos arquivos.
- Abra um terminal ou prompt de comando.
- Navegue até a pasta onde os arquivos foram baixados.
- Execute o arquivo principal:

```bash
python coletor-de-nomes.py
```

## 📝 Licença

Este projeto está licenciado sob a licença **MIT** — veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👤 Autor

Desenvolvido por **HermesRoot**.  










   
