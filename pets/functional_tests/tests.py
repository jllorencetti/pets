import os
from datetime import datetime

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.select import Select

from meupet.models import Kind, Pet
from users.models import OwnerProfile


def get_test_image_file(filename='test.png'):
    from six import BytesIO
    from PIL import Image
    from django.core.files.images import ImageFile

    f = BytesIO()
    image = Image.new('RGB', (200, 200), 'white')
    image.save(f, 'PNG')
    return ImageFile(f, name=filename)

SCREEN_DUMP_LOCATION = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'screendumps')


class SiteTestCases(StaticLiveServerTestCase):
    def setUp(self):
        settings.DEBUG = True
        user = OwnerProfile.objects.create_user('admin', 'ad@min.com', 'admin')
        user.is_information_confirmed = True
        user.save()
        Kind.objects.create(kind='Cats')
        self.browser = webdriver.PhantomJS()
        self.browser.implicitly_wait(1)
        self.browser.maximize_window()

    def tearDown(self):
        if self._test_has_failed():
            if not os.path.exists(SCREEN_DUMP_LOCATION):
                os.makedirs(SCREEN_DUMP_LOCATION)
            for ix, handle in enumerate(self.browser.window_handles):
                self._windowid = ix
                self.browser.switch_to.window(handle)
                self._take_screenshot()
        self.browser.quit()

    def _take_screenshot(self):
        filename = self._get_filename() + '.png'
        print('screenshotting to', filename)
        self.browser.get_screenshot_as_file(filename)

    def _test_has_failed(self):
        for method, error in self._outcome.errors:
            if error:
                return True
        return False

    def _get_filename(self):
        timestamp = datetime.now().isoformat().replace(':', '.')[:19]
        return '{folder}/{classname}.{method}-window{windowid}-{timestamp}'.format(
            folder=SCREEN_DUMP_LOCATION,
            classname=self.__class__.__name__,
            method=self._testMethodName,
            windowid=self._windowid,
            timestamp=timestamp
        )

    def login(self):
        self.browser.get('%s%s' % (self.live_server_url, '/user/login/'))
        name = self.browser.find_element_by_name('username')
        name.send_keys('admin')
        password = self.browser.find_element_by_name('password')
        password.send_keys('admin')
        submit = self.browser.find_element_by_name('login')
        submit.click()
        self.assertIn('Cadastrar Pet', self.browser.page_source)

    def create_pet(self):
        admin = OwnerProfile.objects.first()
        kind = Kind.objects.first()
        pet = Pet(owner=admin, name='Costela', description='Costelinha', kind_id=kind.id,
                  profile_picture=get_test_image_file())
        pet.save()
        return pet

    def test_login(self):
        self.login()
        self.assertIn('Cadastrar Pet', self.browser.page_source)

    def test_add_lost_pet(self):
        self.login()
        self.assertIn('Cadastrar Pet', self.browser.page_source)

        self.browser.get(self.live_server_url + '/pet/lost/')

        name = self.browser.find_element_by_name('name')
        name.send_keys('Test')

        description = self.browser.find_element_by_name('description')
        description.send_keys('Testing')

        kind = self.browser.find_element_by_name('kind')
        kind = Select(kind)
        kind.select_by_index(1)

        profile_picture = self.browser.find_element_by_name('profile_picture')
        profile_picture.send_keys('{}/img/{}.jpg'.format(settings.STATICFILES_DIRS[0], 'sapa'))

        submit = self.browser.find_element_by_name('submit')
        submit.click()

        self.assertIn('Testing', self.browser.page_source)

    def test_add_pet_for_adoption(self):
        self.login()
        self.assertIn('Cadastrar Pet', self.browser.page_source)

        self.browser.get(self.live_server_url + '/pet/adoption/')

        name = self.browser.find_element_by_name('name')
        name.send_keys('Test')

        description = self.browser.find_element_by_name('description')
        description.send_keys('Testing Adoption')

        kind = self.browser.find_element_by_name('kind')
        kind = Select(kind)
        kind.select_by_index(1)

        profile_picture = self.browser.find_element_by_name('profile_picture')
        profile_picture.send_keys('{}/img/{}.jpg'.format(settings.STATICFILES_DIRS[0], 'sapa'))

        submit = self.browser.find_element_by_name('submit')
        submit.click()

        self.assertIn('Testing Adoption', self.browser.page_source)

    def test_logout(self):
        self.login()
        logout_link = self.browser.find_element_by_link_text('Logout')
        logout_link.click()
        self.assertIn('Login', self.browser.page_source)

    def test_edit_own_pet(self):
        # user log in
        self.login()
        self.assertIn('Cadastrar Pet', self.browser.page_source)

        # user register a lost cat with wrong name
        self.browser.get(self.live_server_url + '/pet/lost/')
        self.browser.find_element_by_name('name').send_keys('Wrong Boots')
        self.browser.find_element_by_name('description').send_keys('My dear lovely cat')
        self.browser.find_element_by_name('city').send_keys('Catland')

        # selects the kind as a Cat
        kind = Select(self.browser.find_element_by_name('kind'))
        kind.select_by_index(1)

        # selects the size of the pet
        size = Select(self.browser.find_element_by_name('size'))
        size.select_by_index(3)

        # user select a picture of his cat
        profile_picture = self.browser.find_element_by_name('profile_picture')
        profile_picture.send_keys('{}/img/{}.jpg'.format(settings.STATICFILES_DIRS[0], 'sapa'))

        # click on submit
        self.browser.find_element_by_name('submit').click()

        # user is redirected for the page of his pet and see the wrong name
        # then click on 'Edit' and get redirected for the editing page
        self.browser.find_element_by_link_text('Editar').click()

        # user inform the correct name for the pet then save
        self.browser.find_element_by_name('name').clear()
        self.browser.find_element_by_name('name').send_keys('Fuzzy Boots')
        self.browser.find_element_by_name('submit').click()

        # user see that he is back at the pet page
        self.browser.find_element_by_link_text('Editar')

        # user see the correct name of the cat
        self.assertIn('Fuzzy Boots', self.browser.page_source)
        self.assertIn('Grande', self.browser.page_source)

    def test_edit_profile_information(self):
        # user login
        self.login()

        # user goes to profile page
        self.browser.get(self.live_server_url + '/user/profile/')

        # see a wrong information and click in the edit button
        self.browser.find_element_by_link_text('Editar').click()

        # user change the first name and save it
        self.browser.find_element_by_name('first_name').clear()
        self.browser.find_element_by_name('first_name').send_keys('Super Admin')
        self.browser.find_element_by_name('submit').click()

        # user is back to the profile page and see the correct information
        self.assertIn('Super Admin', self.browser.page_source)

    def test_search_for_a_particular_pet(self):
        # pre register pet
        self.create_pet()

        # user goes to the home
        self.browser.get(self.live_server_url)

        # enter a name in the search form and press enter
        self.browser.find_element_by_name('q').send_keys('Costela\n')

        # user are redirected to the search result page and see the searched pet
        self.assertIn('Costela', self.browser.page_source)

    def test_upload_second_photo(self):
        # pre register pet
        pet = self.create_pet()

        # login
        self.login()

        # go to own pet
        self.browser.get(self.live_server_url + '/pet/{}/'.format(pet.id))

        # upload some new photo
        profile_picture = self.browser.find_element_by_name('another_picture')
        profile_picture.send_keys('{}/img/{}.jpg'.format(settings.STATICFILES_DIRS[0], 'sapa'))

        img_before = len(self.browser.find_elements_by_tag_name('img'))

        submit = self.browser.find_element_by_name('submit')
        submit.click()

        img_after = len(self.browser.find_elements_by_tag_name('img'))

        # verify new photo is showing
        self.assertIn('Outras fotos', self.browser.page_source)
        self.assertEquals(img_after, img_before + 1)
