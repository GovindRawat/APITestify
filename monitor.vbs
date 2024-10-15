Dim folderPath, fso, folder, file, lastModifiedTime

' Specify the folder path to monitor
folderPath = "C:\Path\To\Your\Folder"

Set fso = CreateObject("Scripting.FileSystemObject")
Set folder = fso.GetFolder(folderPath)

' Initialize last modified time
lastModifiedTime = GetLastModifiedTime(folder)

Do
    WScript.Sleep 5000 ' Check every 5 seconds
    If GetLastModifiedTime(folder) <> lastModifiedTime Then
        WScript.Echo "Change detected in folder: " & folderPath
        lastModifiedTime = GetLastModifiedTime(folder)
    End If
Loop

Function GetLastModifiedTime(folder)
    Dim latestTime
    latestTime = 0
    For Each file In folder.Files
        If file.DateLastModified > latestTime Then
            latestTime = file.DateLastModified
        End If
    Next
    GetLastModifiedTime = latestTime
End Function
