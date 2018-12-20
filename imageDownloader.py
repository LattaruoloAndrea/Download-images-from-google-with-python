import urllib.request
import urllib.parse
import os
import re
import sys

# https://github.com/hardikvasa/google-images-download/blob/master/google_images_download/google_images_download.py

# https://github.com/abenassi/Google-Search-API#google-web-search

GOOGLE_SITE = "www.google.it/imghp?hl=it&tab=wi"

GOOGLE_HEADER = "https://www.google.it"

class imageDownloader:
    
    def __init__(self, topic, path, amount, dimension):
        self.topic = topic
        self.path = path
        self.amount = amount
        self.dimension = dimension

    def create_directory(self):
        name_dir = 'images_' + self.topic
        current_path = dir_path = os.path.dirname(os.path.realpath(__file__))
        os.chdir(self.path)
        if not os.path.isdir(name_dir):
            os.mkdir(name_dir)
        os.chdir(current_path)
        return name_dir + '/'

    def download_page(self, url):
        values = {'s': 'basics', 'submit': 'search'}
        data = urllib.parse.urlencode(values)
        data = data.encode('utf-8')
        req = urllib.request.Request(url ,headers={'User-Agent': 'Mozilla/5.0'})
        resp = urllib.request.urlopen(req)
        respData = resp.read()
        data = respData
        if self.amount > 20:
            for i in range(self.amount-10):
                respData2 = resp.read()
                data += respData2
        #debugging
        #file = open('page.txt','w')
        #file.write(str(respData))
        #file.close()
        #debugging
        return str(data)
        #return str(respData)

    def urls_images(self, source_code):
        index_starting = [i.start() for i in re.finditer('src="https:', source_code)] #<a jsname=\"(.*?)\" 
        len_header = len('src="')
        urls_image = []
        url_image = ""
        times = 0
        if self.amount < len(index_starting):
            times = self.amount
        else:
            times = len(index_starting)
        for i in range(30):#times):
            end = source_code.find('\"', index_starting[i]+len_header)
            point = index_starting[i]+len_header
            url_image = source_code[point:end]
            #debugging
            #file = open('url.txt','w')
            #file.write(url_image)
            #file.close()
            #debugging
            urls_image.append(url_image)
        return urls_image 

    def images_download(self, urls_images):
        num = 0
        for i in urls_images:
            full_path = self.path + 'images_'+ self.topic + '/' + self.topic + '_' + str(num) + '.jpg'
            urllib.request.urlretrieve(i,full_path)
            num += 1
            print('Image {0:d} downloaded...'.format(num))

def main():
    id = imageDownloader(sys.argv[1],'images/',30,1000)
    name = id.create_directory()
    url = 'https://www.google.com/search?q=' + id.topic + '+images&source=lnms&tbm=isch'
    id.images_download(id.urls_images(id.download_page(url)))
    print("Immagini scaricate")


if __name__ == '__main__':
    main()
