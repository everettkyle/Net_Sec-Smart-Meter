let data

/*
@function setData() - onclick gets element name and sets data to it to
  prepare for the post request
@param item - html object
*/
function setData(item) {
   data = {name:$.trim($(item).attr('name'))}
   setElement('#SELECTEDPROJECT', $.trim($(item).attr('name')))
}

function setElement(elemID, text) {
  let newText = $(elemID).text().slice(0,19)
  newText += text
  $(elemID).text(newText)
  return
}

function connect() {
  let response
  if(data){
    let password = $('#pswd').val()
    if(password == '') {
      alert('ENTER A PASSWORD')
    }
    data['password'] = password
    $.ajax({
      method:'POST',
      url:'/action?action=CONNECT',
      data:JSON.stringify(data),
      contentType: "application/json",
      success: (result)=> {
              console.log(result)
              response = result
      },
    }).done((result)=>{
      alert(result + ' has been Connected')
      document.location.reload()
    })
  }
}

function disconnect() {
  let response
  if(data){
    let password = $('#pswd').val()
    if(password == '') {
      alert('ENTER A PASSWORD')
    }
    else {
      data['password'] = password
      $.ajax({
        method:'POST',
        url:'/action?action=DISCONNECT',
        data:JSON.stringify(data),
        contentType: "application/json",
        success: (result)=> {
                console.log(result)
                response = result
        },
      }).done(()=>{
        alert(response + ' has been Disconnected')
        document.location.reload()
      })
    }
  }
}

function UpDateFirmWare() {
  if(data){
    $.ajax({
      method:'POST',
      url:'/action?action=UFIRM',
      data:JSON.stringify(data),
      contentType: "application/json",
      success: (result)=> {console.log(result)},
    }).done(()=>{
      alert('Firmware for ' + data['name'] + ' has been updated')
      document.location.reload()
    })
  }
}

function UpDateUse() {
  if(data){
    $.ajax({
      method:'POST',
      url:'/action?action=UPDATEUSE',
      data:JSON.stringify(data),
      contentType: "application/json",
      success: (result)=> {console.log(result)},
    }).done(()=>{
      alert('Usage for ' + data['name'] + ' has been updated')
      document.location.reload()
    })
  }
}


// setSelectedDefault()
