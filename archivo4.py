"""Eto es un archivo de prueba"""
from platform import platform


print(platform())
print(platform(1))
print(platform(0, 1))


from platform import machine
print(machine())

from platform import processor

print(processor())

from platform import system

print(system())

