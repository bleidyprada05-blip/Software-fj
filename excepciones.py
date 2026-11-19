#Excepciones personalizadas 

#Excepción base: atrapándola se cubren todos los errores del sistema.
class ErrorFJ(Exception):
    
#Clientes
class ClienteInvalidoError(ErrorFJ):
  
#ServiciosInvalidos
class ServicioInvalidoError(ErrorFJ):

#ServiciosNoDisponible
class ServicioNoDisponibleError(ErrorFJ):

#ReservaInvalidos
class ReservaInvalidaError(ErrorFJ):

#OperacionNoPermitida
class EstadoReservaError(ErrorFJ):
   
