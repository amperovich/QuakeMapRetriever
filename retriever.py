import requests
from bs4 import BeautifulSoup


def get_links(url: str, extension: str) -> list[str]:
    """
    Получает все ссылки с указанным расширением файла из указанной URL.

    :param url: Входная URL.
    :param extension: Расширение искомых файлов.
    :return: Список ссылок с искомым расширением.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    links = [
        url + link.get("href")
        for link in soup.find_all("a")
        if link.get("href").endswith(extension)
    ]
    return links


def download_files(links: list[str], chunk_size: int = 1024 * 1024) -> None:
    """
    Скачивает файлы по ссылкам и сохраняет их в папку на диск.

    :param links: Список ссылок для скачивания.
    :param chunk_size: Размер куска данных, считываемый за один раз из скачиваемого файла.
    """
    for link in links:
        filename = link.split("/")[-1]
        print(f"Downloading {filename}...")
        with requests.get(link, stream=True) as response:
            response.raise_for_status()
            with open(filename, "wb") as file:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        file.write(chunk)
        print(f"{filename} downloaded successfully.")


if __name__ == "__main__":
    url = "http://q3msk.ru/files/maps/baseq3/"
    extension = ".pk3"
    links = get_links(url, extension)
    download_files(links)
