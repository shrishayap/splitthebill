var i = 1;

function add_name_field(){
  i += 1;
  name_div = document.getElementById('names');
  new_field = document.createElement('input');
  new_name = 'name_' + i;
  new_field.name = new_name;
  new_field.placeholder = 'Name';
  mybr = document.createElement('br');
  name_div.appendChild(mybr);
  name_div.appendChild(new_field);
}


const inpFile = document.getElementById("file");
const previewContainer = document.getElementById("imagePreview");
const previewImage = previewContainer.querySelector(".image-preview__image");
const previewDefaultText = previewContainer.querySelector(".image-preview__default-text");

inpFile.addEventListener('change', function() {
const file = this.files[0];

if (file) {
    const reader = new FileReader();

    previewDefaultText.style.display = 'none';
    previewImage.style.display = 'block';
    
    reader.addEventListener('load', function(){
    console.log(this);
    previewImage.setAttribute('src', this.result);
    });

    reader.readAsDataURL(file);
} else{
    previewDefaultText.style.display = null;
    previewImage.style.display = null;
}
});