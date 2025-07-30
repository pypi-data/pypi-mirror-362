"""
This algorithm was developed and programmed by Ben-Hur Varriano for Sapiens Technology®️
with the goal of providing an “infinite context window” for language models.
The logical foundation of the code is based on extracting features from the prompt and/or a list of dialogues,
retaining only the tokens that best define the message within a predetermined limit. In this way,
the model becomes capable of generalizing the surplus context, assimilating only the general meaning of everything
that was discussed instead of the entire conversation.
This behavior is similar to that of humans, who, although they do not memorize every word in a long conversation,
are able to remember the key points that define what was discussed.

Note: Any public disclosure or comment on the logic and/or operation of this code is strictly prohibited and
the author will be subject to legal proceedings and measures by our team of lawyers.
"""
# --------------------------> A SAPIENS TECHNOLOGY®️ PRODUCTION) <--------------------------
from setuptools import setup, find_packages
package_name = 'sapiens_infinite_context_window'
version = '1.0.4'
setup(
    name=package_name,
    version=version,
    author='SAPIENS TECHNOLOGY',
    packages=find_packages(),
    install_requires=['sapiens-embedding==1.0.7', 'scn==1.0.9'],
    url='https://github.com/sapiens-technology/SapiensInfiniteContextWindow',
    license='Proprietary Software',
    include_package_data=True
)
"""
This algorithm was developed and programmed by Ben-Hur Varriano for Sapiens Technology®️
with the goal of providing an “infinite context window” for language models.
The logical foundation of the code is based on extracting features from the prompt and/or a list of dialogues,
retaining only the tokens that best define the message within a predetermined limit. In this way,
the model becomes capable of generalizing the surplus context, assimilating only the general meaning of everything
that was discussed instead of the entire conversation.
This behavior is similar to that of humans, who, although they do not memorize every word in a long conversation,
are able to remember the key points that define what was discussed.

Note: Any public disclosure or comment on the logic and/or operation of this code is strictly prohibited and
the author will be subject to legal proceedings and measures by our team of lawyers.
"""
# --------------------------> A SAPIENS TECHNOLOGY®️ PRODUCTION) <--------------------------
