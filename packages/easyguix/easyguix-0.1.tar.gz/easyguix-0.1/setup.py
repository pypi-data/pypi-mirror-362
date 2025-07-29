from setuptools import setup, find_packages

setup(
    name="easyguix",
    version="0.1",
    packages=find_packages(),
    install_requires=["pillow", "plyer", "tkcalendar", "tkwebview2"],
    author="Ruzgar",
    description="Basit GUI oluşturmak için kolay Python arayüz kütüphanesi.",
    long_description="Kolay kullanım için tasarlanmış bir GUI kütüphanesi. tkinter + ekstra araçlar ile birleşir.",
    long_description_content_type="text/markdown",
    keywords=["gui", "easy", "tkinter", "simple", "python"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
