function validar_formulario() {
  var email = document.formRegistro.correo;
  var password = document.formRegistro.password;

  var formato_email = /^\w+([\.-]?\w+)@\w+([\.-]?\w+)(\.\w{2,3})+$/;
  if (!email.value.match(formato_email)) {
    alert("Debes ingresar un email electronico valido!");
    email.focus();
    return false; //Para la parte dos, que los datos se conserven
  }

  var passid_len = password.value.length;
  if (passid_len == 0 || passid_len < 8) {
    alert("Debes ingresar una password con mas de 8 caracteres");
    passid.focus();
  }
}

function validarform(){
  var user = document.formRegistro.Nombre;
  var correo = document.formRegistro.correo;
  var clave = document.formRegistro.password;

  var user_len = user.value.length;
  if(user_len == 0 || user_len <8){
      alert("Nombre inválido, el usuario debe tener minimo 8 caracteres");
  }else{
      alert("Usuario Validado correctamente");
  }

  var formatocorreo = /^[-\w.%+]{1,64}@(?:[A-Z0-9-]{1,63}\.){1,125}[A-Z]{2,63}$/i;
  if (!formatocorreo.test(correo.value)){
      alert("Debe ingesar un correo valido")
  }else{
      alert("Correo validado correctamente")
  }

  var pass_len = clave.value.length;
  if(pass_len == 0 || user_len <8){
      alert("Contraseña inválida, la contraseña debe tener minimo 8 caracteres");
  }else{
      alert("Usuario Validado correctamente");
  }
}

