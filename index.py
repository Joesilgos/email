# sudo pip install requests
# sudo pip install beautifulsoup4
import requests
import bs4
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from email.mime.base import MIMEBase
from email import encoders


class NewsEmail:
    def __init__(self):
        self.response = requests.get("https://g1.globo.com/")
        # self.emailFrom =
        self.news = []
        self.status = 200

        # inicia o corpo do email no formato mime com varias parte do email
        self.bodyEmail = MIMEMultipart()
        # inicia o mime application
        self.baseEncode = MIMEBase('application', 'octet-stream')

        # email send se usar o gmail smtp.gmail.com:587
        # self.server = smtplib.SMTP("smtp.mailtrap.io", 2525)
        self.server = smtplib.SMTP("smtp.gmail.com", 587)

        if self.response.status_code == 200:
            self.document = bs4.BeautifulSoup(
                self.response.content, 'html.parser')
            self.scraping()

        else:
            self.status = self.response.status_code
            print("error", self.response.status_code)

    def scraping(self):
        # pega a class que contem as principais noticias
        tagDivs = self.document.findAll("div", class_="bastian-feed-item")

        for tagDiv in tagDivs:
            # pega a tag que contém o titulo e o link
            title = tagDiv.find("a", class_="feed-post-link").text
            link = tagDiv.find("a", class_="feed-post-link")['href']
            # pega a imagem e verifica se ela contém image se a image é uma image de tag de video ou uma tag img
            preview = tagDiv.find("div", class_="_preempt-visibility")
            if(preview):
                preview = preview.find("video")['poster']
            else:
                preview = tagDiv.find("img", class_="bstn-fd-picture-image")
                if(preview):
                    preview = preview['src']
                else:
                    preview = ""
            # pega a tag que contem o subtitulo e verifica se ele existe
            subTitle = tagDiv.find("div", class_="feed-post-body-resumo")
            if(subTitle):
                subTitle = subTitle.text
            else:
                subTitle = ""

            # pega o assunto e verifica se ele existe
            subject = tagDiv.find("span", class_="feed-post-header-chapeu")
            if(subject):
                subject = subject.text
            else:
                subject = ""

            # salva as informações da noticia atual em um dicionario e adiciona ela a lista news
            self.news.append({"title": title, "link": link, 'image': preview,
                             'subTitle': subTitle, 'subject': subject})

    def mimeContent(self):
        
        
        # bodyEmail['From'] = "61013ff9f1-7ac134@inbox.mailtrap.io"
        self.bodyEmail['From'] = "joesilgos@gmail.com"
        self.bodyEmail['To'] = "joesilgos@gmail.com"
        self.bodyEmail['Subject'] = "Notícias G1 com webscraping em python"
        # por padrão o mimetext vem como fromato plain text
        content = ""
        for new in self.news:
            content += f'<div style="margin-bottom:10px;"><div><div><a href=""style="text-decoration:none;color:black;font-size:24px;font-family:ui-monospace;">{new["title"]}</a></div><span style="color:#6f6f6f;">{new["subTitle"]}</span></div></div>'

        self.bodyEmail.attach(MIMEText(content, 'html'))
    def fileAttach(self, filename):
        # abri o arquivo
        attach = open("/media/joesilgos/PROJETOS8/services/desafio/file.txt", 'rb')
        
        # carrega o documento de anexo
        self.baseEncode.set_payload(attach.read())
        # codifica o documento no formato base64 para ser enviado pelo email
        encoders.encode_base64(self.baseEncode)
        #adiciona o cabeçalho da requisição com o nome arquivo enviado por anexo
        self.baseEncode.add_header('Content-Disposition', f'attachment; filename={attach.name}')
        attach.close()
        self.bodyEmail.attach(self.baseEncode)
    def send(self, email, password):
        
        # ativa protocolo de segurança que criptografa e-mails gmail etc necessita o uso
        self.server.ehlo()
        self.server.starttls()
        # credenciais de login
        # server.login("fe47b77804e9b8", "1ec4823a0e2271")
        self.server.login(email, password)

        self.mimeContent()

        self.fileAttach("/media/joesilgos/PROJETOS8/services/desafio/file.txt")
        

        # envia o email
        self.server.sendmail(self.bodyEmail['From'], self.bodyEmail['To'], self.bodyEmail.as_string())
        # fecha o email para nao deixar processos ativos quando o script terminar
        self.server.quit()

email = NewsEmail()
email.send("joesilgos@gmail.com", "Developer12345")