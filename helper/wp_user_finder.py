import requests

class WPUserFinder:

    def __init__(self, target_url):
        self.target_url = target_url
        self.user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0'

    def find_from_wp_json(self):
        end_point  = '/wp-json/wp/v2/users/'
        target_url = self.target_url

        with requests.get(target_url + end_point, headers = {'user-agent' : self.user_agent}) as request:
            if request.status_code == 200:
                for json in request.json():
                    found_user = []
                    found_user.append(json['slug'])
                    return found_user
            else:
                return []

    def find_from_author_page(self):
        count = 1
        end_point  = '/?author='
        target_url = self.target_url
        found_username = set()

        while True:
            url_endpoint = target_url + end_point + str(count)
            with requests.get(url_endpoint, headers = {'user-agent' : self.user_agent}, allow_redirects = True) as request:
                if request.status_code == 200:
                    if request.url != url_endpoint:
                        user_name = request.url
                        user_name = user_name.split('/')[-2]
                        found_username.add(user_name)
                    else:
                        break
                else:
                    break
            count += 1

        return list(found_username)
