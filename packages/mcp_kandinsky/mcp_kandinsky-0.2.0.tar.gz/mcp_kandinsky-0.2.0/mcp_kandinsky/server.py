from mcp.server.fastmcp import FastMCP
import asyncio
from .kandinsky_api import KandinskyAPI
import os
import base64

mcp = FastMCP("mcp_kandinsky")
api = KandinskyAPI()

@mcp.tool()
async def kandinsky_generate_image(
    prompt: str,
    filename: str,
    project_dir: str,
    width: int = 1024,
    height: int = 1024,
    style: str = "DEFAULT",
    negative_prompt: str = "",
    overwrite: bool = False
) -> str:
    """
    Генерирует изображение по текстовому описанию через Kandinsky API и сохраняет его в папку kandinsky внутри project_dir.
    Параметры:
      - prompt: текстовый запрос
      - filename: имя файла для сохранения (например, cat.png)
      - project_dir: абсолютный путь к папке проекта
      - width, height: размеры изображения
      - style: стиль генерации (DEFAULT, KANDINSKY, UHD, ANIME)
      - negative_prompt: негативный промпт (опционально)
      - overwrite: перезаписывать ли файл, если он уже существует
    Возвращает сообщение об успехе или причине отказа.
    """
    if not os.path.isabs(project_dir):
        return "project_dir должен быть абсолютным путём."
    folder = os.path.join(project_dir, "kandinsky")
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    if os.path.exists(filepath) and not overwrite:
        return f"Файл {os.path.relpath(filepath, project_dir)} уже существует. Установите overwrite=True для перезаписи."
    # Генерируем изображение
    files = await asyncio.to_thread(
        api.generate_and_get_image,
        prompt, width, height, style, negative_prompt
    )
    if not files or not files[0]:
        return "Ошибка генерации изображения."
    # Сохраняем файл
    try:
        with open(filepath, "wb") as f:
            f.write(base64.b64decode(files[0]))
    except Exception as e:
        return f"Ошибка сохранения файла: {e}"
    return f"Изображение успешно сгенерировано и сохранено в {os.path.relpath(filepath, project_dir)}."

def run():
    mcp.run(transport="stdio") 