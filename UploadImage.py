import re, os, sys, math, time, datetime, shutil
from pattern.web import URL, DOM, plaintext, extension, Element, find_urls
from contextlib import closing
from selenium.webdriver import Firefox, chrome
from selenium.webdriver.support.ui import WebDriverWait


class BoxImageUrl(object):
    def __init__(self):
        self.share_folder_url = 'https://app.box.com/s/jlwchpjfcpueq1gshij7'  # use to go to box to get the image url
        self.box_image_full_url = ''
        self.box_image_start_url = 'https://app.box.com/representation/file_version_'
        self.box_image_end_url = ''

        self.local_image_store_path = r'G:\waterfall1.jpg'
        self.image_version = '0'  # current version that exists
        self.image_version_history = '0'  # Use to check version or whether file has already uploaded.

        self.dom_object = object()

        self.url_query_timeout = 0
        self.new_image_upload_check_cntdn = 10  # number of times before the while loop break for checking.

    def set_box_public_link_of_image(self, image_public_link):
        self.share_folder_url = image_public_link

    def fetch_image_url_fr_box(self):
        with closing(Firefox()) as browser:
            browser.get(self.share_folder_url)
            time.sleep(3)
            page_source = browser.page_source

        self.set_box_image_end_url(page_source)
        self.set_final_image_box_url()

    def set_box_image_end_url(self, box_page_source):
        dom = DOM(box_page_source)

        img_element = dom("img")[0]
        txt_str = img_element.attributes['src'].encode()
        self.image_version = re.search('file_version_(.*)/image', txt_str).group(1)
        self.box_image_end_url = re.search('file_version_(.*)', txt_str).group(1)

    def set_final_image_box_url(self):
        self.box_image_full_url = self.box_image_start_url + self.box_image_end_url

    def set_image_version_history(self):
        self.fetch_image_url_fr_box()  # will also set the image version history
        self.image_version_history = self.image_version
        print 'Image version history', self.image_version_history

    def upload_new_image(self, target_image_path):
        print 'uploading images'
        shutil.copy2(target_image_path, self.local_image_store_path)
        if self.has_img_uploaded():
            print 'Successful'
        else:
            print 'new image not found'

    def has_img_uploaded(self):
        for n in range(self.new_image_upload_check_cntdn):
            time.sleep(10)
            self.fetch_image_url_fr_box()
            if not self.image_version == self.image_version_history:
                return True
        return False