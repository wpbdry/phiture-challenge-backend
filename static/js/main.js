function switchTab(tabId, tabContentId) {
    //Display correct content
    var contentTabs = document.getElementsByClassName("tab-content");
	for (var i=0; i<contentTabs.length; i++) {
		contentTabs[i].style.display = "none";
	}
    document.getElementById(tabContentId).style.display = "block";
    //Highlight correct tab button
	var tabMenuItems = document.getElementsByClassName("tab-menu");
	for (var i=0; i<tabMenuItems.length; i++) {
		tabMenuItems[i].className = "tab-menu"; 
	}
	document.getElementById(tabId).className = "tab-menu active";
}