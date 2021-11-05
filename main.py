# sudo pip install requests 
# sudo pip install beautifulsoup4 
import requests
import bs4
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from email.mime.base import MIMEBase
from email import encoders

#carrega a url do G1 que retorna uma class reponse da pagina 
response = requests.get("https://g1.globo.com/")

news = []
if response.status_code == 200:
    
    document = bs4.BeautifulSoup(response.content, 'html.parser')

    #pega a class que contem as principais noticias
    tagDivs = document.findAll("div", class_ = "bastian-feed-item")

    for tagDiv in tagDivs:
        #pega a tag que contém o titulo e o link
        title = tagDiv.find("a", class_ = "feed-post-link").text
        link = tagDiv.find("a", class_ = "feed-post-link")['href']
        # pega a imagem e verifica se ela contém image se a image é uma image de tag de video ou uma tag img
        preview = tagDiv.find("div", class_ = "_preempt-visibility")
        if(preview):
            preview = preview.find("video")['poster']
        else:
            preview = tagDiv.find("img", class_ = "bstn-fd-picture-image")
            if(preview):
                preview = preview['src']
            else:
                preview = ""
        # pega a tag que contem o subtitulo e verifica se ele existe
        subTitle = tagDiv.find("div", class_ = "feed-post-body-resumo")
        if(subTitle):
            subTitle = subTitle.text
        else: subTitle = ""

        # pega o assunto e verifica se ele existe 
        subject = tagDiv.find("span", class_ = "feed-post-header-chapeu")
        if(subject):
            subject = subject.text
        else: subject = ""
                
        # salva as informações da noticia atual em um dicionario e adiciona ela a lista news
        news.append( { "title" : title, "link" : link, 'image': preview, 'subTitle' : subTitle, 'subject' : subject } )
    


    #email send se usar o gmail smtp.gmail.com:587
    # server = smtplib.SMTP("smtp.mailtrap.io", 2525)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    # ativa protocolo de segurança que criptografa e-mails gmail etc necessita o uso
    server.ehlo()
    server.starttls()
    #credenciais de login
    # server.login("fe47b77804e9b8", "1ec4823a0e2271")
    server.login("joesilgos@gmail.com", "Noivogaysou12345")

    #inicia o corpo do email no formato mime com varias parte do email
    bodyEmail = MIMEMultipart()
    # bodyEmail['From'] = "61013ff9f1-7ac134@inbox.mailtrap.io"
    bodyEmail['From'] = "joesilgos@gmail.com"
    bodyEmail['To'] = "joesilgos@gmail.com"
    bodyEmail['Subject'] = "Notícias G1 com webscraping em python"
    # por padrão o mimetext vem como fromato plain text
    content = ""
    for new in news:
        content += f'<div style="margin-bottom:10px;"><div><div><a href=""style="text-decoration:none;color:black;font-size:24px;font-family:ui-monospace;">{new["title"]}</a></div><span style="color:#6f6f6f;">{new["subTitle"]}</span></div></div>'

    bodyEmail.attach(MIMEText(content, 'html'))

    # abri o arquivo
    # attach = open("/media/joesilgos/PROJETOS8/services/desafio/file.txt", 'rb')
    # baseEncode = MIMEBase('application', 'octet-stream')
    # # carrega o documento de anexo
    # baseEncode.set_payload(attach.read())
    # # codifica o documento no formato base64 para ser enviado pelo email 
    # encoders.encode_base64(baseEncode)
    # #adiciona o cabeçalho da requisição com o nome arquivo enviado por anexo
    # baseEncode.add_header('Content-Disposition', f'attachment; filename={attach.name}')
    # attach.close()
    # bodyEmail.attach(baseEncode)

    #envia o email
    server.sendmail(bodyEmail['From'], bodyEmail['To'], bodyEmail.as_string())
    #fecha o email para nao deixar processos ativos quando o script terminar
    server.quit()





    

else:
    print("error", response.status_code)
