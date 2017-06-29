Attribute VB_Name = "GlyphsOrderCalculations"
Option Explicit

Type GlyphsAppInfo
    Name As String
    USV As String
    sort As Double
End Type

Private GlyphData As Worksheet ' GlyphData spreadsheet

Sub test()
    Dim d As New Scripting.Dictionary
    
    d("x") = 42
    d(42) = "forty-two"
    Debug.Print d("x")
    Set d = Nothing
End Sub

' Calculate sort order that closely matches Glyphs default sort order.

' Second attempt. Now we'll pay attention to the Glyphs-sort order only for our encoded glyphs, and try to
' fit all contextual/alternate forms next to their encoded glyph.

Sub ComputeGlyphNames2()
    
    Dim r As New Scripting.Dictionary   ' dictionary of root silnames and their sort number from Glyphs
    Dim e As New Scripting.Dictionary   ' dictionary of extensions and their sort offsets
    Dim eOffset As Double              ' last-used extension sort offset
    eOffset = 0
    
    'Open "testFile" For Output As #1

    Set GlyphData = Application.Workbooks.Open("C:\Reference\Typography\GlyphData.xlsx", False, True).Worksheets(1)
    
    Dim Row As Integer, Col As Integer
    
    Dim W As Worksheet      ' absGlyphList spreadsheet
    Application.Workbooks("absGlyphList.xlsm").Activate
    Set W = Application.ActiveSheet
    Col = WorksheetFunction.Match("GlyphsAppName", W.Range("1:1"), 0)
    
    Dim silName As String, Root As String, Ctx As String, Ext As String, newName As String, newCtx As String
    Dim pos As Double, sort As Double, USV As String
    Dim result As GlyphsAppInfo
    
    Row = 2
    While Len(W.Cells(Row, 1).Value) > 0
'    While (Row < 20)
        silName = W.Cells(Row, 1).Value
        Ext = ""
        If (Left(silName, 1) = "#") Then
            W.Cells(Row, Col + 2) = "Comment"
            GoTo Loop1
        End If
            
        ' first let's just see if the name already matches Glyphs
        result = FindGlyph(Name:=silName)
        If result.sort > 0 Then
            ' yes it does!
            'Debug.Print sfmt(silName, 20); "MATCH: SORT = "; result.Sort
            W.Cells(Row, Col) = result.Name
            W.Cells(Row, Col + 1) = result.sort
            'record results for subsequent entries:
            r(silName) = result.sort
            r(result.sort) = silName
            GoTo Loop1
        End If
        
        ' Does this glyph have a Unicode value?
        USV = W.Cells(Row, 3)
        If Len(USV) > 0 Then
            result = FindGlyph(USV:=USV)
            If result.sort > 0 Then
                'Debug.Print sfmt(silName, 20); "USV = "; sfmt(USV, 6); " newName = "; result.Name, " SORT = "; result.Sort
                W.Cells(Row, Col) = result.Name
                W.Cells(Row, Col + 1) = result.sort
                'record results for subsequent entries:
                r(silName) = result.sort
                r(result.sort) = silName
            Else
                'Debug.Print sfmt(silName, 20); "USV = "; sfmt(USV, 6); " not found in GlyphsApp"
                'Print #1, "not found:", "USV = "; sfmt(USV, 7); "("; silName; ")"
                W.Cells(Row, Col + 2) = "USV not found"
            End If
            GoTo Loop1
        End If
        
        ' No USV. have to find root of silName, look up its USV
        Root = silName
        
        ' Split the extension off the name
        pos = InStr(Root, ".")
        If pos > 1 Then
            Ext = Mid(Root, pos, 99)
            Root = Left(Root, pos - 1)
        End If

        ' Split off contextual/alternate form
        Ctx = Right(Root, 3)
        If Ctx = "Fin" Then
            Root = Left(Root, Len(Root) - 3)
            sort = 0.001
        ElseIf Ctx = "Med" Then
            Root = Left(Root, Len(Root) - 3)
            sort = 0.002
        ElseIf Ctx = "Ini" Then
            Root = Left(Root, Len(Root) - 3)
            sort = 0.003
        ElseIf Right(Root, 6) = "Medium" Then
            Root = Left(Root, Len(Root) - 6)
            Ctx = "Medium"
            sort = 0.004
        ElseIf Right(Root, 5) = "Small" Then
            Root = Left(Root, Len(Root) - 5)
            Ctx = "Small"
            sort = 0.005
        Else
            ' Contextual/alternate form unknown
            Ctx = ""
            sort = 0
        End If
        
        ' See if we can find this root in our own data
        ' If so
        '   Try to find the root's entry in Glyphs
        '   If found
        '      Construct proposed GlyphsApp name
        '      Construct proposed sort order: entry{sortorder} + . (my row - root row)
        
        ' Now see if we have seen this root yet:
        If r.Exists(Root) Then
            ' found it!
            sort = sort + r(Root)
        Else
            ' No root found -- can't go further
            'Debug.Print sfmt(Root + Ctx, 20); " ( Ext = "; Ext; ") Ctx ROOT NOT FOUND"
            'Print #1, "root not found:", Root + Ctx, 20, " ( Ext = "; Ext; ")"
            W.Cells(Row, Col + 2) = "not found"
            GoTo Loop1
        End If
        
        ' make up a sort offset, if it doesn't already exist, for this extension
        If Len(Ext) > 0 And Not e.Exists(Ext) Then
            eOffset = eOffset + 0.01
            e(Ext) = eOffset
        End If
        sort = sort + e(Ext)
        
        W.Cells(Row, Col + 1) = sort
        
                
Loop1:   Row = Row + 1
    Wend

End Sub

' This first attempt assumed that for all USVs known to glyphData.xml, all the required contextual forms would be
' present in the xml, but this is not the case.

Sub ComputeGlyphNamesOriginal()
    Open "testFile" For Output As #1

    Set GlyphData = Application.Workbooks.Open("C:\Reference\Typography\GlyphData.xlsx", False, True).Worksheets(1)
    
    Dim Row As Integer, Col As Integer
    
    Dim W As Worksheet      ' absGlyphList spreadsheet
    Application.Workbooks("absGlyphList.xlsm").Activate
    Set W = Application.ActiveSheet
    Col = WorksheetFunction.Match("GlyphsAppName", W.Range("1:1"), 0)
    
    Dim silName As String, Root As String, Ctx As String, Ext As String, newName As String, newCtx As String
    Dim pos As Double, USV As String
    Dim result As GlyphsAppInfo
    
    Row = 2
    While Len(W.Cells(Row, 1).Value) > 0
'    While (Row < 20)
        silName = W.Cells(Row, 1).Value
        Ext = ""
        If (Left(silName, 1) = "#") Then
            W.Cells(Row, Col + 2) = "Comment"
            GoTo Loop1
        End If
            
        ' first let's just see if the name already matches Glyphs
        result = FindGlyph(Name:=silName)
        If result.sort > 0 Then
            ' yes it does!
            'Debug.Print sfmt(silName, 20); "MATCH: SORT = "; result.Sort
            W.Cells(Row, Col) = result.Name
            W.Cells(Row, Col + 1) = result.sort
            GoTo Loop1
        End If
        
        ' Does this glyph have a Unicode value?
        USV = W.Cells(Row, 3)
        If Len(USV) > 0 Then
            result = FindGlyph(USV:=USV)
            If result.sort > 0 Then
                'Debug.Print sfmt(silName, 20); "USV = "; sfmt(USV, 6); " newName = "; result.Name, " SORT = "; result.Sort
                W.Cells(Row, Col) = result.Name
                W.Cells(Row, Col + 1) = result.sort
            Else
                'Debug.Print sfmt(silName, 20); "USV = "; sfmt(USV, 6); " not found in GlyphsApp"
                'Print #1, "not found:", "USV = "; sfmt(USV, 7); "("; silName; ")"
                W.Cells(Row, Col + 2) = "USV not found"
            End If
            GoTo Loop1
        End If
        
        ' No USV. have to find root of silName, look up its USV
        Root = silName
        
        ' Split the extension off the name
        pos = InStr(Root, ".")
        If pos > 1 Then
            Ext = Mid(Root, pos, 99)
            Root = Left(Root, pos - 1)
        End If

        ' Split off contextual/alternate form
        Ctx = Right(Root, 3)
        If Ctx = "Ini" Then
            Root = Left(Root, Len(Root) - 3)
            newCtx = ".init"
        ElseIf Ctx = "Med" Then
            Root = Left(Root, Len(Root) - 3)
            newCtx = ".medi"
        ElseIf Ctx = "Fin" Then
            Root = Left(Root, Len(Root) - 3)
            newCtx = ".fina"
        ElseIf Right(Root, 5) = "Small" Then
            Root = Left(Root, Len(Root) - 5)
            Ctx = ""
            Ext = ".small" + Ext
        ElseIf Right(Root, 6) = "Medium" Then
            Root = Left(Root, Len(Root) - 6)
            Ctx = ""
            Ext = ".medium" + Ext
        Else
            ' Contextual/alternate form unknown
            Ctx = ""
        End If
        
        ' See if we can find this root in our own data
        ' If so
        '   Try to find the root's entry in Glyphs
        '   If found
        '      Construct proposed GlyphsApp name
        '      Construct proposed sort order: entry{sortorder} + . (my row - root row)
        
        
        Dim RootRow As Integer
        RootRow = 0
        On Error Resume Next
        RootRow = WorksheetFunction.Match(Root, W.Range("A:A"), 0)
        On Error GoTo 0 ' re-enable errors
        If RootRow = 0 Then
            ' No root found -- can't go further
            'Debug.Print sfmt(silName, 20); " (Ctx = "; Ctx; " Ext = "; Ext; ") ROOT NOT FOUND"
            'Print #1, "root not found", silName; " (Ctx = "; Ctx; " Ext = "; Ext; ")"
            W.Cells(Row, Col + 2) = "not found"
            GoTo Loop1
        End If
        
        ' found the root of the SIL name -- get its USV
        USV = WorksheetFunction.Index(W.Range("C:C"), RootRow)
        If Len(USV) = 0 Then
            ' No USV found -- can't go further
            'Debug.Print sfmt(silName, 20); " (Ctx = "; Ctx; " Ext = "; Ext; ") has no USV"
            'Print #1, "no USV:", silName; " (Ctx = "; Ctx; " Ext = "; Ext; ")"
            W.Cells(Row, Col + 2) = "No USV"
            GoTo Loop1
        End If
        
        ' Ok, we know the root's USV. Get root of its new name
        Dim newRoot As String
        result = FindGlyph(USV:=USV)
        If result.sort = 0 Then
            'Debug.Print sfmt(silName, 20); "USV = "; sfmt(USV, 6); " not found in GlyphsApp"
            'Print #1, "not found:", "USV = "; sfmt(USV, 7); "("; silName; ")"
            W.Cells(Row, Col + 2) = "USV not found"
            GoTo Loop1
        End If
        newRoot = result.Name
        
        ' Two cases:  a contextual form (init, medi, fina) or not; either may be alternates
        If (Len(Ctx) > 0) Then
            ' contextual form -- find the correct root row in our own list:
            RootRow = 0
            On Error Resume Next
            RootRow = WorksheetFunction.Match(Root + Ctx, W.Range("A:A"), 0)
            On Error GoTo 0 ' re-enable errors
            If RootRow = 0 Then
                ' No root found -- can't go further
                'Debug.Print sfmt(Root + Ctx, 20); " ( Ext = "; Ext; ") Ctx ROOT NOT FOUND"
                'Print #1, "root not found:", Root + Ctx, 20, " ( Ext = "; Ext; ")"
                W.Cells(Row, Col + 2) = "not found"
                GoTo Loop1
            End If
            ' and adjust new name to include contextual form
            newRoot = newRoot + newCtx
        End If
        
        ' Finally we should be able to find this [possibly-contextual form] name in Glyph's list
        
        result = FindGlyph(Name:=newRoot)
        If result.sort = 0 Then
            'Debug.Print sfmt(newRoot, 20); " not found!"
            'Print #1, "not found:", newRoot, "("; silName; ")"
            ' but we do know the name, so put it in our spreadsheet:
            W.Cells(Row, Col) = newRoot + Ext
            W.Cells(Row, Col + 2) = "not found"
        Else
            'Debug.Print sfmt(silName, 20); " newName = "; newRoot + Ext; " SORT = "; result.Sort + ((Row - RootRow) / 1000)
            W.Cells(Row, Col) = newRoot + Ext
            W.Cells(Row, Col + 1) = result.sort + ((Row - RootRow) / 1000)
        End If
                
Loop1:   Row = Row + 1
    Wend
    Close #1

End Sub

' Search GlyphData.xml for a name or USV

' return GlyphsAppInfo structure:
'   if .sort == 0, name wasn't found

Function FindGlyph(Optional Name As String = "", Optional USV As String = "") As GlyphsAppInfo
    Dim res As GlyphsAppInfo
    On Error Resume Next
    If Len(Name) > 0 Then
        res.sort = WorksheetFunction.Match(Name, GlyphData.Range("A:A"), 0)
    ElseIf Len(USV) > 0 Then
        res.sort = WorksheetFunction.Match(USV, GlyphData.Range("D:D"), 0)
    Else
        res.sort = 0
    End If
    On Error GoTo 0 ' re-enable errors
    
    If res.sort > 0 Then
        ' Found it!
        res.Name = GlyphData.Cells(res.sort, 1).Value
        res.USV = GlyphData.Cells(res.sort, 4).Value
    End If
    FindGlyph = res
End Function


Function sfmt(s As String, l As Integer)
    If Len(s) >= l Then
        sfmt = s
    Else
        sfmt = s + Space(l - Len(s))
    End If
End Function


