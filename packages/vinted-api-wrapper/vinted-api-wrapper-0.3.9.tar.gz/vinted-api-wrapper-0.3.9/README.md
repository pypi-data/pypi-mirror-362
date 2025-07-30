<a name="readme-top"></a>


<!-- PROJECT SHIELDS -->
<p align="center">
  <a href="https://github.com/Pawikoski/vinted-api-wrapper/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/Pawikoski/vinted-api-wrapper.svg?style=for-the-badge" alt="Contributors">
  </a>
  <a href="https://github.com/Pawikoski/vinted-api-wrapper/network/members">
    <img src="https://img.shields.io/github/forks/Pawikoski/vinted-api-wrapper.svg?style=for-the-badge" alt="Forks">
  </a>
  <a href="https://github.com/Pawikoski/vinted-api-wrapper/stargazers">
    <img src="https://img.shields.io/github/stars/Pawikoski/vinted-api-wrapper.svg?style=for-the-badge" alt="Stargazers">
  </a>
  <a href="https://github.com/Pawikoski/vinted-api-wrapper/issues">
    <img src="https://img.shields.io/github/issues/Pawikoski/vinted-api-wrapper.svg?style=for-the-badge" alt="Issues">
  </a>
  <a href="https://github.com/Pawikoski/vinted-api-wrapper/pulls">
    <img src="https://img.shields.io/github/issues-pr/Pawikoski/vinted-api-wrapper?style=for-the-badge" alt="Pull Requests">
  </a>
  <a href="https://github.com/Pawikoski/vinted-api-wrapper/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/Pawikoski/vinted-api-wrapper.svg?style=for-the-badge" alt="License">
  </a>
</p>

<p align="center">
  <a href="https://pypi.org/project/vinted-api-wrapper/">
    <img src="https://img.shields.io/pypi/v/vinted-api-wrapper?style=for-the-badge" alt="PyPi">
  </a>
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/python-3.10%2B-blue?style=for-the-badge" alt="Python">
  </a>
</p>



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Pawikoski/vinted-api-wrapper">
    <img src="images/image.png" alt="Logo" height="80">
  </a>

<h3 align="center">Vinted Api Wrapper</h3>

  <p align="center">
    Simple client for Vinted Developer API written in Python
    <br />
    <a href="https://github.com/Pawikoski/vinted-api-wrapper"><strong>« Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Pawikoski/vinted-api-wrapper/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/Pawikoski/vinted-api-wrapper/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>📋 Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## ℹ️ About The Project

The Vinted API Wrapper is a Python-based tool designed to interact with the Vinted marketplace. It provides a set of methods for fetching product data, user information, and catalog details directly from Vinted's API. The wrapper streamlines the process of making API requests, handling cookies, and parsing JSON responses into structured Python `dataclass` objects. It enables developers to search, filter, and retrieve data efficiently, making it easier to integrate Vinted's functionalities into their own applications.

<p align="right">(<a href="#readme-top">back to top ⬆️</a>)</p>



## ⚙️ Built With

[![Python][Python]][Python-url]
[![requests][requests]][requests-url]
[![dacite][dacite]][dacite-url]

<p align="right">(<a href="#readme-top">back to top ⬆️</a>)</p>



<!-- GETTING STARTED -->
## 🟢 Getting Started & Installation

To use the Vinted API Wrapper you can clone the repository or use `pip` package (recommended)

1. Install `vinted-api-wrapper` package
```sh
pip install vinted-api-wrapper
```
2. Usage: Import the Vinted class into your Python script and start making API calls:
```python
from vinted import Vinted
vinted = Vinted()
```
* To specify the Vinted marketplace domain for API requests, pass the desired domain when initializing the Vinted object. By default, the domain is set to vinted.pl. However, you can choose from the following supported domains:
```python
["pl", "fr", "at", "be", "cz", "de", "dk", "es", "fi", "gr", "hr", "hu", "it", "lt", "lu", "nl", "pt", "ro", "se", "sk", "co.uk", "com"]

# Usage example:
vinted = Vinted(domain="fr")
```

* To use a proxy for API requests, you can configure it when initializing the Vinted object:
```python
# Configure proxy settings
proxy_settings = {
    'username': 'your_proxy_username',
    'password': 'your_proxy_password',
    'host': 'proxy_host',
    'port': 'proxy_port'
}

# Create proxy URL
proxy_url = f"http://{proxy_settings['username']}:{proxy_settings['password']}@{proxy_settings['host']}:{proxy_settings['port']}"

# Initialize Vinted with proxy
vinted = Vinted(domain="fr", proxy=proxy_url)
```

<p align="right">(<a href="#readme-top">back to top ⬆️</a>)</p>



<!-- USAGE EXAMPLES -->
## ❓Usage

Using `vinted-api-wrapper` in Your Project

The Vinted class provides several useful methods to interact with Vinted's API. Below are some key methods and examples:

* Search for Products: Search the Vinted marketplace by keywords and filters OR search url (more in docs).
    ```python
    items = vinted.search(query="sneakers", catalog_ids=1, brand_ids=100)
    # SearchResponse(code=0, pagination=Pagination(...), dominant_brand=DominantBrand(...), items=[Item(id=1234567890, title='Nike shoes', price='35.0', is_visible=True, discount=None, brand_title='Nike', user=User(id=987654, login='foobar', ...more), url='https://www.vinted.pl/items/1234567890-nike-shoes', promoted=False, photo=ItemPhoto(...), favourite_count=0, service_fee='4.65', total_item_price='39.65', view_count=0, content_source='search',, search_tracking_params=SearchParams(...)), Item(...)], search_tracking_params=SearchTrackingParams(...)
    ```
* Get User Information: Retrieve details about a specific user.
    ```python
    user = vinted.user_info(12345)
    # UserResponse(code=0, pagination=None, user=DetailedUser(id=12345, anon_id='xyz123', login='foobar', real_name=None, email=None, birthday=None, item_count=70, given_item_count=20, taken_item_count=5, followers_count=4, following_count=15, following_brands_count=1, positive_feedback_count=8, neutral_feedback_count=0, negative_feedback_count=0, ...more))
    ```
* Retrieve Item Details: Fetch detailed information about a specific item by its ID.

    ```python
    user = vinted.item_info(12345)
    # ItemsResponse(code=0, pagination=None, item=DetailedItem(id=5146387299, title='New Rock 38 38,5 buty na platformie nowe goth punk', brand_id=432, size_id=58, status_id=6, user_id=124343433, ...more))
    ```

<!-- TODO: _For more examples, please refer to the [Documentation](https://example.com)_ -->

<p align="right">(<a href="#readme-top">back to top ⬆️</a>)</p>



<!-- CONTRIBUTING -->
## 🌱 Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top ⬆️</a>)</p>

## 🏆 Top contributors:

<a href="https://github.com/pawikoski/vinted-api-wrapper/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=pawikoski/vinted-api-wrapper" alt="contrib.rocks image" />
</a>



<!-- LICENSE -->
## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top ⬆️</a>)</p>



<!-- CONTACT -->
## 📥 Contact
  
<a href="mailto:pawikoski@gmail.com">
    <img src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Gmail">
</a>
<a href="https://linkedin.com/in/paweł-stawikowski">
    <img src="https://img.shields.io/badge/-LinkedIn-blue?style=for-the-badge&logo=Linkedin&logoColor=white" alt="LinkedIn">
</a>
<p align="right">(<a href="#readme-top">back to top ⬆️</a>)</p>




<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/Pawikoski/vinted-api-wrapper.svg?style=for-the-badge
[contributors-url]: https://github.com/Pawikoski/vinted-api-wrapper/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Pawikoski/vinted-api-wrapper.svg?style=for-the-badge
[forks-url]: https://github.com/Pawikoski/vinted-api-wrapper/network/members
[stars-shield]: https://img.shields.io/github/stars/Pawikoski/vinted-api-wrapper.svg?style=for-the-badge
[stars-url]: https://github.com/Pawikoski/vinted-api-wrapper/stargazers
[issues-shield]: https://img.shields.io/github/issues/Pawikoski/vinted-api-wrapper.svg?style=for-the-badge
[issues-url]: https://github.com/Pawikoski/vinted-api-wrapper/issues
[license-shield]: https://img.shields.io/github/license/Pawikoski/vinted-api-wrapper.svg?style=for-the-badge
[license-url]: https://github.com/Pawikoski/vinted-api-wrapper/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/paweł-stawikowski
[product-image]: images/image.png
[Python]: https://img.shields.io/badge/python-000000?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://python.org/
[dacite]: https://img.shields.io/badge/dacite-20232A?style=for-the-badge&logo=github&logoColor=61DAFB
[dacite-url]: https://github.com/konradhalas/dacite
[requests]: https://img.shields.io/badge/requests-35495E?style=for-the-badge&logo=github&logoColor=4FC08D
[requests-url]: https://github.com/psf/requests
