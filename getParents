function myFunction() {
  while (folders.hasNext()) {
    var folders = DriveApp.getFolders();
    var folder = folders.next();
    Logger.log(folder.getName());
    myFunc();
    
  }
}
function myFunc() {
  var parents = folder.getParents();
  while (parents.hasNext()) {
      var parent = parents.next();
      Logger.log('Parent: ' + parent.getName());
      
    }
}
