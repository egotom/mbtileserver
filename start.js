var sh = WScript.CreateObject("WScript.Shell"); 
var wmi = GetObject("winmgmts://./root/CIMv2");

//sh.Run("net start MongoDB",0);
while(true){
	var node = wmi.ExecQuery("Select * From Win32_Process where name='mbtileserver.exe'");
	//WScript.Echo(node.Count);
	if(node.Count==0) sh.Run("D:\\work\\mbtileserver\\mbtileserver.exe",0);
}