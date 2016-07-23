import os
from datetime import datetime

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from meupet.models import Kind, Pet, City
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
        self.test_city, _ = City.objects.get_or_create(city='Araras')
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

    def select_dropdown(self, element_name, index):
        element = Select(self.browser.find_element_by_name(element_name))
        element.select_by_index(index)

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

    def test_register_pet(self):
        self.login()
        self.assertIn('Cadastrar Pet', self.browser.page_source)

        self.browser.get(self.live_server_url + '/pets/novo/')

        name = self.browser.find_element_by_name('name')
        name.send_keys('Test')

        description = self.browser.find_element_by_name('description')
        description.send_keys('Testing Adoption')

        self.select_dropdown('status', 1)

        self.select_dropdown('kind', 1)

        self.select_dropdown('city', 1)

        profile_picture = self.browser.find_element_by_name('profile_picture')
        profile_picture.send_keys('{}/img/{}.png'.format(settings.STATICFILES_DIRS[0], 'logo'))

        submit = self.browser.find_element_by_name('submit')
        submit.click()

        self.assertIn('Obrigado', self.browser.page_source)

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
        self.browser.get(self.live_server_url + '/pets/novo/')
        self.browser.find_element_by_name('name').send_keys('Wrong Boots')
        self.browser.find_element_by_name('description').send_keys('My dear lovely cat')

        # select the city
        self.select_dropdown('city', 1)

        # selects the kind as a Cat
        self.select_dropdown('kind', 1)

        # selects the size of the pet
        self.select_dropdown('size', 3)

        # selects the sex of the pet
        self.select_dropdown('sex', 1)

        # user select a picture of his cat
        profile_picture = self.browser.find_element_by_name('profile_picture')
        profile_picture.send_keys('{}/img/{}.png'.format(settings.STATICFILES_DIRS[0], 'logo'))

        # click on submit
        self.browser.find_element_by_name('submit').click()

        # assert pet was registered
        self.browser.find_element_by_link_text('aqui').click()
        self.assertIn('Wrong Boots - Desaparecido', self.browser.page_source)

        # user is redirected for the page of his pet and see the wrong name
        # then click on 'Edit' and get redirected for the editing page
        self.browser.find_element_by_link_text('Editar').click()

        # user change the status to 'For Adoption'
        self.select_dropdown('status', 1)

        # user inform the correct name for the pet then save
        self.browser.find_element_by_name('name').clear()
        self.browser.find_element_by_name('name').send_keys('Fuzzy Boots')
        self.browser.find_element_by_name('submit').click()

        # user see that he is back at the pet page
        self.browser.find_element_by_link_text('Editar')

        # user see the correct name of the cat
        self.assertIn('Fuzzy Boots', self.browser.page_source)
        self.assertIn('Grande', self.browser.page_source)
        self.assertIn('Fêmea', self.browser.page_source)
        self.assertIn('Araras', self.browser.page_source)
        self.assertIn('Fuzzy Boots - Para Adoção', self.browser.page_source)

    def test_edit_profile_information(self):
        # user login
        self.login()

        # user goes to profile page
        self.browser.get(self.live_server_url + '/user/profile/')

        # see a wrong information and click in the edit button
        self.browser.find_element_by_link_text('Editar').click()

        # user change the first name
        self.browser.find_element_by_name('first_name').clear()
        self.browser.find_element_by_name('first_name').send_keys('Super')

        # user change the last name
        self.browser.find_element_by_name('last_name').send_keys('Admin')

        # and submit
        self.browser.find_element_by_name('submit').click()

        # user is back to the profile page and see the correct information
        self.assertIn('Alterações gravadas com sucesso.', self.browser.page_source)

    def test_upload_second_photo(self):
        # pre register pet
        pet = self.create_pet()

        # login
        self.login()

        # go to own pet
        self.browser.get(self.live_server_url + '/pets/{}/'.format(pet.slug))

        # upload some new photo
        profile_picture = self.browser.find_element_by_name('another_picture')
        profile_picture.send_keys('{}/img/{}.png'.format(settings.STATICFILES_DIRS[0], 'logo'))

        img_before = len(self.browser.find_elements_by_tag_name('img'))

        submit = self.browser.find_element_by_name('submit')
        submit.click()

        img_after = len(self.browser.find_elements_by_tag_name('img'))

        # verify new photo is showing
        self.assertIn('Outras fotos', self.browser.page_source)
        self.assertEquals(img_after, img_before + 1)

    def test_create_new_city(self):
        self.login()

        self.browser.get(self.live_server_url + '/pets/novo/')

        name = self.browser.find_element_by_name('name')
        name.send_keys('Test New City')

        description = self.browser.find_element_by_name('description')
        description.send_keys('Testing Adoption')

        self.select_dropdown('status', 1)

        self.select_dropdown('kind', 1)

        show_new_city = self.browser.find_element_by_id('new-city')
        show_new_city.click()

        new_city = self.browser.find_element_by_id('id_new_city')
        new_city.send_keys('Created City')

        profile_picture = self.browser.find_element_by_name('profile_picture')
        profile_picture.send_keys('{}/img/{}.png'.format(settings.STATICFILES_DIRS[0], 'logo'))

        submit = self.browser.find_element_by_name('submit')
        submit.click()

        self.assertIn('Obrigado', self.browser.page_source)

        self.browser.get(self.live_server_url + '/pets/')

        self.assertIn('Created City', self.browser.page_source)

    def test_delete_pet(self):
        # pre register pet
        pet = self.create_pet()

        # login
        self.login()

        # go to own pet
        self.browser.get(self.live_server_url + '/pets/{}/'.format(pet.slug))

        # click on delete button
        self.browser.find_element_by_css_selector('button.btn.btn-danger').click()
        WebDriverWait(self.browser, 2).until(ec.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input.btn-danger'))
        )

        # confirm the delete action
        self.browser.find_element_by_css_selector('input.btn-danger').click()

        self.assertNotIn('Costela', self.browser.page_source)
