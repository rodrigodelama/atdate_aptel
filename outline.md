# Práctica global de Aplicaciones Telemáticas: Servicio de hora en Internet

## Introducción
Esta práctica consiste en desarrollar un programa que funcione tanto de cliente como de servidor del protocolo TIME. El protocolo TIME, definido en 1983 en la RFC 868, es un protocolo estándar del IETF cuyo propósito es proporcionar información de fecha y hora en formato usable por un ordenador.

La práctica debe desarrollarse en **lenguaje C** o en **python** sobre sistema operativo **Linux** y **debe funcionar en los ordenadores de los laboratorios docentes de Ingeniería Telemática**, donde se realizará la corrección. Recordad que para poder trabajar en estos laboratorios debéis tener una cuenta abierta en el departamento.

## Objetivos
Los objetivos que se pretenden alcanzar con el desarrollo de esta práctica son los siguientes:

1. Enfrentarse a la implementación de un protocolo real, partiendo de su especificación original (RFC).
2. Conocer protocolos de servicio de hora en internet.
3. Adquirir conocimientos de programación de sockets.
4. Reforzar conocimientos teóricos de algunos de los protocolos que hemos visto en la asignatura (UDP, TCP, ...).

## Enunciado
El protocolo TIME está especificado en la [RFC 868](https://www.ietf.org/rfc/rfc826). Es necesario desarrollar un programa que cumpla con las especificaciones de dicho documento y ciertas consideraciones adicionales que serán descritas a continuación.

El programa a desarrollar podrá funcionar en dos modos: **modo consulta** y **modo servidor**:

- En ***modo consulta***, el programa debe seguir el flujo de operación de un cliente TIME sobre TCP o sobre UDP, dependiendo de los parámetros de ejecución. 
En el caso de ejecución como **cliente UDP**, el programa operará tal y como se describe en la RFC, es decir: enviará un datagrama vacío al servidor y obtendrá la respuesta.

    En el caso de ejecución como **cliente TCP**, el programa tendrá el comportamiento descrito en la RFC pero con una ligera modificación: no cierra la conexión inmediatamente después de obtener la hora del servidor, sino que se queda escuchando actualizaciones de la hora hasta que el usuario envía una señal SIGINT para finalizar el programa. En ambos casos, la fecha y hora obtenidas deberán mostrarse por pantalla siguiendo el formato que se detalla más abajo en el apartado de "Ejemplos y trazas".

- En ***modo servidor***, el programa deberá funcionar como un **servidor TIME sobre TCP** de la siguiente manera: cada vez que un cliente se conecte, el servidor le enviará la hora (obtenida de su sistema local) cada segundo hasta que el cliente decida cerrar la conexión.

**Ejecutable y parámetros:** el ejecutable se llamará **atdate** y debe soportar los siguientes parámetros: *atdate [-s serverhost] [-p port] [-m cu | ct | s ] [-d]*

- -s serverhost: nombre del servidor TIME al que se conectará el programa para obtener la fecha y hora actual. Este argumento es obligatorio sólo si el programa se lanza en modo consulta, es decir, con -m cu o -m ct.
- -m: para indicar el modo de ejecución del programa:
  - cu: el programa arranca en modo consulta funcionando como cliente UDP.
  - ct: el programa arranca en modo consulta funcionando como cliente TCP.
  - s: el programa arranca en modo servidor.
  - Si no se especifica la opción -m, el programa arranca en modo consulta UDP, es decir: -m cu.

- -p port: para indicar el número de puerto.
  - Si se arranca en modo consulta, indica que el servidor TIME al que nos conectamos escucha en un puerto diferente al 37.
  - Si se arranca en modo servidor, indica el puerto en el que quedará a la escucha el servidor.
  - Si no se especifica se usará el puerto por defecto, es decir, 37.

- -d: modo depuración. Mostrará trazas adicionales para la depuración del programa.
Si alguno de los parámetros opcionales necesarios para la ejecución no se proporciona por línea de comandos, se tomarán los valores por defecto.

## Ejemplos y trazas:

- Modo consulta UDP:

    monitor01:~> atdate -s time-a.timefreq.bldrdoc.gov -m cu

    Mon Feb 7 19:45:31 CET 2016
- Modo servidor:
  
    monitor01:~> atdate -m s -p 6001

    TIME server running in port 6001

- Modo consulta TCP:

    Nos conectamos al servidor lanzado en el paso anterior ejecutando otra instancia del programa en modo consulta TCP:

    monitor02:~> atdate -s monitor01.lab.it.uc3m.es -p 6001 -m ct
    
    Mon Feb 7 19:46:12 CET 2016
    
    Mon Feb 7 19:46:13 CET 2016
    
    Mon Feb 7 19:46:14 CET 2016
    
    Mon Feb 7 19:46:15 CET 2016

    SIGINT received, closing program

## Notas y aclaraciones a la RFC:

1. Como vuestros usuarios no tienen permisos de root, no podéis lanzar un servidor escuchando en un puerto por debajo de 1024. Para evitar colisiones con servidores de otros estudiantes, os aconsejamos usar como puerto para vuestras pruebas el 6000 + las tres últimas cifras de vuestro NIA.
2. El servidor debe ser concurrente.
3. Para trabajar con los datos relativos a las fechas pueden ser útiles las siguientes funciones: time(2), strftime(3).
4. Tenga en cuenta a la hora de procesar las fechas que la "Época" de Unix es diferente a la tomada como referencia en el protocolo TIME. **En el primer caso es el 1 de Enero de 1970**, mientras que en el segundo caso, se utiliza el 1 de Enero de 1900. Consulte la RFC.
5. Existen multitud de servidores de hora en Internet que implementan el protocolo TIME que pueden ser usados para probar el correcto funcionamiento de su programa. A continuación listamos algunos ejemplos, puntualmente algunos de ellos pueden no estar disponibles:

     - time-a.timefreq.bldrdoc.gov
     - time-b.timefreq.bldrdoc.gov
     - time-c.timefreq.bldrdoc.gov
     - utcnist.colorado.edu
     - ntps1-2.uni-erlangen.de
     - time.ien.it
     - ptbtime2.ptb.de

6. Es recomendable realizar pruebas con el cliente rdate (man rdate para más información) instalado en aulas para comprender bien el protocolo antes de proceder con la implementación. El análisis de tráfico con tcpdump puede ser de gran ayuda en esta tarea. Un ejemplo de ejecución de rdate preguntando al servidor time-a.timefreq.bldrdoc.gov sería:

    monitor01:~> rdate -u -p time-a.timefreq.bldrdoc.gov
    
    Tue Sep  4 09:09:38 CEST 2018

7. No es necesario que el programa fije la fecha en el sistema local, es suficiente con mostrarla por pantalla.

# Evaluación
La nota de esta práctica de evaluación continua tendrá un **peso del 10%** sobre la nota final de la asignatura. La evaluación se realizará de **forma individual** en un laboratorio, se solicitará que se realice una modificación de la práctica para que su comportamiento sea ligeramente distinto y se corregirá el correcto funcionamiento de esta modificación. La realización correcta de la práctica sin la modificación no puntúa.

## Fechas importantes:

La evaluación de esta práctica se va a realizar los días **5 de octubre a las 11:00 - 13:00 (primer intento) y 9 de noviembre a la 13:00 - 15:00 (segundo intento)** siguiendo el modelo de evaluación anterior. 

El código de la práctica original (dos días antes de la prueba de evaluación) y el de la modificación deberá entregarse por Aula Global al finalizar el examen. Se habilitarán los enlaces correspondientes a estas entregas en Aula Global.

## Condiciones de entrega práctica original:

- Se debe entregar **un único fichero de forma individual** en formato zip. El nombre del fichero será nia.zip, donde nia será el número de vuestro NIA, por ejemplo 100123456.zip
- El fichero *zip* contendrá los siguientes ficheros:
     - Los ficheros .c, y .h necesarios para generar el ejecutable de la práctica.
     - Un fichero Makefile.
     - Un fichero README con el nombre y correo del alumno y, de forma opcional, unos breves comentarios sobre la práctica: aspectos adicionales a los del enunciado que se implementen, o cualquier tema fuera de lo común que debamos tener en cuenta durante la corrección (el formato de este fichero es libre).
El zip y el Makefile deben ser tales que, habiendo copiado el zip a un directorio vacío, la siguiente secuencia de comandos genere un fichero binario atdate en ese mismo directorio listo para ejecutar:
unzip grupo01.zip
make
El programa no debe tener errores de compilación.
Es recomendable que el ejecutable no tenga fugas de memoria. Se puede comprobar con valgrind.

Las condiciones de entrega de la modificación se especificarán en el examen.

# Recursos y enlaces
## Sobre Sockets
- [Guía Beej de Programación en Redes](http://beej.us/guide/bgnet/)
- Capítulos 6, 7 y 8 de "[Linux Socket Programming](http://proquest.safaribooksonline.com/0-672-31935-7)" de Sean Walton, Sams Publishing Co. 2001 (disponible sólo desde la Universidad)

## Sobre el protocolo TIME
- [RFC 868](https://www.ietf.org/rfc/rfc826): Time protocol