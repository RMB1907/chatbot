# setup.ps1 

$folders = @("data", "scripts", "app")

Write-Output "Creating folders..."
foreach ($folder in $folders) {
    if (!(Test-Path -Path $folder)) {
        New-Item -ItemType Directory -Path $folder | Out-Null
        Write-Output "Created folder: $folder"
    }
}

Write-Output "`nCreating starter files..."
$files = @(
    "scripts\scrape_proverbs.py",
    "app\vectorstore.py",
    "app\rag_chain.py",
    "app\retriever.py",
    "app\ui.py",
    "main.py",
    ".env",
    ".gitignore",
    "README.md"
)

foreach ($file in $files) {
    New-Item -ItemType File -Path $file -Force | Out-Null
    Write-Output "Created file: $file"
}

Write-Output "`nCreating virtual environment..."
python -m venv venv

Write-Output "`nActivating environment..."
. .\venv\Scripts\Activate.ps1

Write-Output "`nInstalling dependencies..."
pip install --upgrade pip
pip install requests sentence-transformers langchain openai faiss-cpu tiktoken python-dotenv

Write-Output "`nSetup complete."
