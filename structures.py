#
PROCESS_NO_DIC = {
1:"Simple Tray",
2:"Trans.A",
3:"Rotary",
4:"CamE Escape",
5:"Cam D/H Escape",
6:"Lubricant A1",
7:"Lubricant A2",
8:"Lubricant B",
9:"Robot1",
10:"Trans.B",
11:"PWB Root",
12:"PWB Top",
13:"SliderB escape",
14:"SliderC",
15:"SliderA/D",
16:"Robot2",
17:"Chain exchanger",
18:"Trans.C",
19:"Holder press",
20:"Lever Lubricant",
21:"Case/Cover",
22:"ScrewA",
23:"Robot3",
}
#
EVENT_NO_DIC = {
1:"A0",
2:"A1",
3:"A2",
4:"B0",
5:"B1",
9:"D00",
10:"D01",
11:"D02",
13:"D04",
14:"D05",
15:"D06",
16:"D16",
24:"D15",
34:"E00",
35:"E01",
36:"E02",
37:"E03",
}
#
EVENT_DIC = {
1:"Mass Production Start",
2:"Mass Production Finish",
3:"Edit screen switch",
4:"Model change",
5:"Operation mode change",
9:"Origin return start",
10:"Origin return finish",
11:"Origin return Err",
13:"1 cycle start",
14:"Continoues operation start",
15:"1cycle operation is completed",
16:"Log messeage",
24:"Error reset",
34:"Production counter Up",
35:"Quantity counter Up",
36:"NG counter Up",
37:"Increment arbitrary counter",
}

# processNo = 1000
# try:
#     print(PROCESS_NO_DIC[int(processNo)])
# except KeyError as e:
#     print(f"Get_Device_Fromm_Process({processNo}): A machine with this processNo is not defined")
#     print(processNo)
