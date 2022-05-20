// String to send to python flask endpoint
test = 'Hello';
// find ax - the 'unmask' button to send the image to python flask endpoint
var ax = document.getElementById('ax');
// if the button exists, attach the makePostRequest event
if (ax) {
  ax.addEventListener("click", makePostRequest, false);
}
// Same as above, however for the choosefile event
var bx = document.getElementById('bx');
if (bx) {
  bx.addEventListener("click", choosefile, false);
}
// Import sharp library
const sharp = require('sharp');

// Post request to Flask Endpoint
async function makePostRequest(test) {
  // Disable button to prevent new requests being sent while the old one is still processing
  document.getElementById('ax').disabled = true;
  // If cropper is loaded
  if (cropper) {
    // Get the data from the cropped area of the image
    let c = cropper.getData(true);
    // Use the chosen constraints from cropper to crop and save the image
    sharp(filepath[0]).extract({ width: c.width, height: c.height, left: c.x, top: c.y }).toFile("out/image.jpg")
      // Once the file has been saved, make axios post request
      .then(function (new_file_info) {
        axios.post('http://127.0.0.1:5000/repaint')
          // Once Python flask endpoint has finished unmasking the image
          .then(function (response) {
            // Undisable the 'Unmask' button
            document.getElementById('ax').disabled = false;
            // Destroy cropper overlay
            if (cropper) {
              cropper.destroy();
            }
            // Set image to be the output file from Flask Endpoint
            document.getElementById('image').src = response.data;
          })
          // Error catching
          .catch(function (error) {
            console.log(error);
          });
      })
      .catch(function (err) {
        console.log(err);
      });
  }
}
// Import ipc renderer and cropper
const { ipcRenderer } = require('electron');
Cropper = require('cropperjs');
// Create cropper variable so is visable by the makePostRequest function
var cropper;
// Choosefile function
function choosefile() {
  // Send openfile event to main, with specified file type filter
  ipcRenderer.send('open-file', {
    title: 'Choose an Image',
    defaultPath: '',
    filters: [
      { name: 'Images', extensions: ['png', 'jpg', 'jpeg'] }
    ]
  });
  // Display image event
  ipcRenderer.on('display-file', (event, data) => {
    // retrieve image filepath
    filepath = data.filePaths;
    // Get placeholder
    let placeholder = document.getElementById('placeholderImage');
    // Remove placeholder image shown at start
    if (placeholder) {
      placeholder.remove();
    }
    // Destroy pre-existing cropper overlay
    if (cropper) {
      cropper.destroy();
    }
    // Display image
    document.getElementById('image').src = filepath;
    // Enable unmask button
    document.getElementById('ax').disabled = false;
    // Create new cropper overlay on image
    cropper = new Cropper(image, {
      aspectRatio: 1,
      zoomable: false,
      movable: false,
    });
  });

}