# PipeBio Python SDK

![image](https://github.com/pipebio/api-examples/actions/workflows/main.yml/badge.svg)

![image](https://uploads-ssl.webflow.com/628cfc9c7bfe1d60e1cfa130/638cff6c65a7e46c4e82aeae_PipeBio_Logo_Black_RGB.png)

A Python 3.9+ SDK for the [PipeBio](https://pipebio.com/) platform.

![image](https://uploads-ssl.webflow.com/628cfd01406f3f5bb9c8477d/63a332531a1b2c3d7b9bf86b_Year%20in%20review%20-%20PipeBio%20feature%20releases%20in%202022-p-800.jpg)

The integrated bioinformatics platform for large molecule and peptide discovery

PipeBio is an integrated cloud-based platform for biologics discovery that allows wet lab scientists to easily analyze antibody and peptide sequences with functional assay data and bioinformaticians to deploy their own code and run workflows.

Use PipeBio to configure standard analysis workflows and create SOPs with the range bioinformatics tools on PipeBio for

* Antibody sequence analysis and discovery
* Antibody engineering
* Short peptide discovery
* NGS, Sanger, PacBio and single cell sequence analysis

### Installation
```
pip install pipebio
```

### Examples
Example usage of the sdk can be found at [api-examples](https://github.com/pipebio/api-examples).

### Environment Variables
In order to use the sdk, you should get an api key from the [me](https://app.pipebio.com/AbLabs/me) page.

This can then be used by either: 
* setting as a system wide environment variable `EXPORT PIPE_API_KEY=*****`.
* setting in the command line when you run your scripts `PIPE_API_KEY=***** python your_script.py`.
* using an .env file - this sdk will automatically load the contents of an .env file (**must** be called `.env` and in the same directory as your script) and set any environment variables set in it.

Example .env file
```text
PIPE_API_KEY=*****
```

### Extending the sdk
If the endpoint you need is not currently supported by the sdk, then session is available in the pipebio_client, 
which can be used in the usual requests style e.g.:
```python
from pipebio.pipebio_client import PipebioClient

# PipebioClient initialises by reading the PIPE_API_KEY environment variable for authorization.
# Please ensure this is set (see Environment Variables section for how).
client = PipebioClient(url='https://app.pipebio.com')

# Session already has the base url set, so you need to use the relevant part of the route as your url.
# So when the below api request is made, it is translated to https://app.pipebio.com/api/v2/me'
response = client.session.get(url='me')
print(response.json())
```

### Support
Please contact <support@pipebio.com> for help.