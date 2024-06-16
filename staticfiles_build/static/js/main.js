let slider = document.getElementById ('myRange');
let output = document.getElementById ('rangeValue');

output.innerHTML = 'Compress Size: ' + slider.value + '%'; // Display the default slider value

slider.oninput = function () {
  output.innerHTML = 'Compress Size: ' + this.value + '%';
};

// REPASTE THIS FUNCTION, NEW LINES ADDED

function previewFile () {
  const fileInput = document.getElementById ('selectImage');
  const preview = document.getElementById ('preview');
  const uploadIcon = document.getElementById ('uploadIcon');
  const uploadLoader = document.getElementById ('uploadLoader');

  // Clear previous preview
  preview.innerHTML = '';

  // Show loader and hide preview initially
  preview.classList.add('hidden');
  uploadLoader.classList.remove('hidden');
  uploadIcon.classList.remove ('hidden')

  const file = fileInput.files[0];
  const fileName = file.name;

  if (file) {
    const reader = new FileReader ();

    reader.onloadend = function () {
       // Hide loader and show preview
       preview.classList.remove('hidden');
       uploadLoader.classList.add('hidden');
      uploadIcon.classList.add ('hidden');

      const img = document.createElement ('img');
      img.classList.add ('file-preview');
      img.src = reader.result;
      img.alt = `Preview of ${fileName}`;
      preview.appendChild (img);

      const name = document.createElement ('p');
      let sizeApproxKb = file.size / 1024;
      let sizeApproxMb = file.size / (1024 * 1024);
      name.textContent = `${fileName} - ${sizeApproxKb < 1024 ? sizeApproxKb.toFixed(2) + "KB" : sizeApproxMb.toFixed(2) + "MB"}`;
      preview.appendChild (name);
    }

    reader.readAsDataURL (file);
  }
};
