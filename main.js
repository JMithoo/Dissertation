// Import child process spawning
var spawn = require("child_process").spawn;
// Spawn python child and run the pipeline python script
var python = spawn('python',["Pipeline.py"]);
  // print data output by the python code
  python.stdout.on('data', function (data) {
    console.log("data: ", data.toString('utf8'));
  });
  // print any errors in the python code
  python.stderr.on('data', (data) => {
    console.log(`stderr: ${data}`); // when error
  });

// Import electron
const { app, BrowserWindow } = require('electron')

// Create a 500x600 electron window  
function createWindow () {
 const win = new BrowserWindow({
 width: 500,
 height: 600,
 webPreferences: {
  nodeIntegration: true,
  contextIsolation: false,
  enableRemoteModule: true
 }
 })
// Load index.html into the window
win.loadFile('index.html')
// Remove menu containing file, edit ect...
win.removeMenu();
}
// Code handling creation and destruction of window
app.whenReady().then(createWindow)
app.on('window-all-closed', () => {
  // Kill python code on window close
  python.kill('SIGINT');
// Mac handling to allow mac users to close to taskbar.
 if (process.platform !== 'darwin') {
 app.quit()
 }
})
// Create electron window
app.on('activate', () => {
 if (BrowserWindow.getAllWindows().length === 0) {
 createWindow()
 }
})

// Import ipc main and file dialoge
const { ipcMain } = require('electron');
const { dialog } = require('electron');
// When open-file even is ran, open file dialog and
// display the image by calling open-file-paths event
ipcMain.on('open-file',(event,data)=>{
  dialog.showOpenDialog(null, data).then(filePaths => {
      event.sender.send('display-file', filePaths);
  });
});