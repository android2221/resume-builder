document.addEventListener("DOMContentLoaded", function(event) { 
  console.log("this is JS land");

  const Editor = require('tui-editor'); 
  
  const instance = new Editor({
    initialEditType: "markdown",
    previewStyle: 'vertical',
    height: '300px',
    el: document.querySelector('#editorSection')
  });
  
  instance.getHtml();
});

