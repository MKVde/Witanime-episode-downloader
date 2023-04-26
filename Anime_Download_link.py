import sys
import os
import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QFileDialog, QVBoxLayout
from PyQt5.QtGui import QIcon

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Anime Downloader")
        self.setWindowIcon(QIcon("C:\\Users\\abdir\\OneDrive\\Desktop\\Web Dev\\Web Scraping Learn\\Extract mega link from the website\\THE APP\\witanime_favicon.ico"))
        self.setGeometry(100, 100, 600, 400) # x, y, width, height
        app_icon = QIcon("C:\\Users\\abdir\\OneDrive\\Desktop\\Web Dev\\Web Scraping Learn\\Extract mega link from the website\\THE APP\\witanime_favicon.ico")
        app.setWindowIcon(app_icon)

        # Create labels and input fields
        url_label = QLabel("Anime URL:", self)
        self.url_input = QLineEdit(self)
        
        provider_label = QLabel("Provider:", self)
        self.provider_combo = QComboBox(self)
        self.provider_combo.addItems(["mega", "google", "mediafire"])

        path_label = QLabel("Save path:", self)
        self.path_input = QLineEdit(self)
        self.path_button = QPushButton("Browse", self)
        self.path_button.clicked.connect(self.select_path)
        
        run_button = QPushButton("Run", self)
        run_button.clicked.connect(self.run_script)
        
        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(url_label)
        layout.addWidget(self.url_input)
        layout.addWidget(provider_label)
        layout.addWidget(self.provider_combo)
        layout.addWidget(path_label)
        layout.addWidget(self.path_input)
        layout.addWidget(self.path_button)
        layout.addWidget(run_button)
        self.setLayout(layout)
    
    def select_path(self):
        path = QFileDialog.getExistingDirectory(self, "Select folder")
        self.path_input.setText(path)
        
    def run_script(self):
        # Get user input values
        url = self.url_input.text()
        provider = self.provider_combo.currentText()
        save_path = self.path_input.text()
        
        # Send a GET request to the URL and get the response
        response = requests.get(url)

        # Use BeautifulSoup to parse the response HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all the episode links on the page
        episode_links = soup.select(".episodes-card-title a")

        # Create a directory to store the text files if it doesn't exist
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # Extract anime name from URL
        anime_name = url.split('/')[-2]

        # Loop through each episode URL
        for episode_link in episode_links:
            episode_url = episode_link["href"]

            # Make a GET request to the episode page
            response = requests.get(episode_url)

            # Parse the HTML using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all HTML elements containing the provider link
            provider_links = soup.find_all('a', href=lambda href: href and provider in href)

            # Extract the second link from the list of provider links
            if len(provider_links) >= 2:
                download_link = provider_links[1]['href']
                episode_num = episode_link.text.split(' ')[-1]
                print(f"Download link for Episode {episode_num}: {download_link}")

                # Write the download link to a text file
                filename = f"{anime_name}.txt"
                file_path = os.path.join(save_path, filename)
                with open(file_path, "a") as f:
                    f.write(f"Episode {episode_num}: {download_link}\n")
            else:
                episode_num = episode_link.text.split(' ')[-1]
                print(f"No 'downlaod' link found in Episode {episode_num}")

                # Write an error message to a text file
                filename = f"{anime_name}.txt"
                file_path = os.path.join(save_path, filename)
                with open(file_path, "a") as f:
                    f.write(f"No 'downlaod' link found in Episode {episode_num}\n")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
