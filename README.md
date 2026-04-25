# Netcat.py

*Fecha de publicación: 30/12/2025*

> [!NOTE]
> **Iker Marín López (IML15)**
>
> Cybersecurity Engineer (Universidad Rey Juan Carlos)
>
> **Links:** 🔗 [LinkedIn](https://www.linkedin.com/in/iker-marin-lopez-90791b379/) | 🐱 [GitHub](https://github.com/IML15) | 📥 [Telegram](https://t.me/hueco44)


This repository shows a python design which substitutes the famous application "Netcat". This practice is really interesting for users who want to introduce their shelf's into the hacking environment.


> [!WARNING]
> **ADVERTENCIA:** Este documento ha sido realizado con fines exclusivamente educativos en un entorno controlado. El autor no se hace responsable del mal uso de la información aquí expuesta.


- **Sugerencia**: si no se dispone de un Rubber Ducky, también podríais desactivar el Windows defender manualmente siguiendo los pasos del [payload](#payload) (adjuntado más adelante) y probar el comando que ejecuta la Reverse Shell como práctica (así podrías verificar el funcionamiento de la Reverse Shell y estudiar el mismo).

## 1. Preparación de las máquinas (Atacante y Víctima)

Crearemos dos máquinas en **VMware** (en nuestro caso una Kali-Linux [atacante] y una máquina Windows11 “25H2” [víctima]) y las configuraremos de modo que las máquinas compartan la misma red en uno de sus adaptadores red (este segundo adaptador lo crearemos antes de iniciar las máquinas). En mi caso, he creado una red llamada “Red InternaIML15” que será la que usen ambas máquinas y que además será de uso privado para el host (nosotros). 


