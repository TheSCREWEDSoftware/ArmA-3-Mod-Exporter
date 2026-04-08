### Made and tested with Python 3.12.4

# ArmA 3 Mod Exporter

Simple tool to extract and export the list of mods currently loaded in a running Arma 3 session, including both mod names and Steam Workshop IDs.

## Usage

1. Place this script in any folder.
2. Run the script while Arma 3 is running with your desired mods loaded.
3. The script will prompt you to define your Arma directory and Workshop directory (currently using two .txt files: `path.txt` and `workshop_path.txt`).
   - `path.txt`: Should contain the path to your Arma 3 installation. The script checks for the presence of at least one of the following executables: `arma3.exe`, `arma3_x64.exe`, or `arma3battleye.exe`.
   - `workshop_path.txt`: Should contain the path to your Steam Workshop mods folder (must include `workshop\content\107410` and be on the same drive as the game path).
4. At least one of the Arma 3 executables must be running, and at least one mod must be loaded for the script to work.
5. After validation, you'll see:

```
Do you wish to see the list and/or save them to a file?
  1 - See List
  2 - Save to File
  3 - See the list and save to a file
  Q - Quit
```

### Example Output (Choice: 3)

```
--- Active Mods (76) ---
  1 - @RHSAFRF [ ID: 843425103 ]
  2 - @RHSUSAF [ ID: 843577117 ]
  3 - @CBA_A3 [ ID: 450814997 ]
  ...
  76 - @Gruppe Adler Captive Walking [ ID: 2134489854 ]
```

#### Example contents of [08_04_2026_modsWithName.txt](08_04_2026_modsWithName.txt)
```
"-mod=@RHSAFRF;@RHSUSAF;@CBA_A3;@RKSL Studios - Attachments v3.02;@3CB BAF Weapons;@3CB BAF Vehicles;@3CB BAF Equipment;@RHSGREF;@WMO - Walkable Moving Objects;@Swim Faster;@Task Force Timberwolf Female Characters;@[MELB] Mission Enhanced Little Bird;@3DEN Attributes Fast Load;@3den Enhanced;@Accurate Arsenal-Eden Icons;@ace;@AI avoids prone;@Antistasi - The Mod;@Arsenal Search;@ZEI - Zeus and Eden Interiors;@JSRS SOUNDMOD;@Ladder Tweak 2x;@JCA - Hand Flares;@Enhanced Map;@EnhancedTrenches;@Drongos Spooks and Anomalies;@Brighter Flares;@DHI Uniforms and Equipment;@No Weapon Sway;@Reduced Haze Mod v3.1;@Red Squadron - Target Pack;@Red Squadron - Target Pack Zeus Compat;@3CB BAF Units;@RHSSAF;@3CB BAF Units (RHS compatibility);@3CB BAF Vehicles (RHS reskins);@3CB BAF Weapons (RHS ammo compatibility);@3CB Factions;@KAT - Advanced Medical;@ACRE2;@Turret Enhanced;@ShackTac User Interface (DISCONTINUED);@ACE 3 Extension (Animations and Actions);@ACE 3 Extension (Placeables);@Gruppe Adler Trenches;@ACE Trench compat;@ACE Vehicle Medical;@ACE3 Arsenal Extended - Core;@Additional Zeus Things (Zeus Enhanced & Ares Achilles);@Zeus Enhanced;@Air Support Plus;@Alternative Running;@Zeus Additions;@Improved Melee System;@WebKnight's Zombies and Creatures;@Webknight Units - LAMBS_Danger.fsm Compatibility Patch (+ ACE3 Support);@WebKnight Flashlights and Headlamps;@Weather Plus;@Sci-fi Support Plus;@Remove stamina;@Remove stamina - ACE 3;@Prone Launcher;@Hide Among The Grass - HATG;@Fire Support Plus;@AI Stow NVGs;@Better Inventory;@Brush Clearing;@Crows Zeus Additions;@Freefall Fix;@Freestyles Crash Landing;@No More Aircraft Bouncing;@NIArms All In One (V14 Onwards);@Advanced Vault System- Remastered;@BackpackOnChest;@GRAD Sling Helmet;@Gruppe Adler Captive Walking"
```

#### Example contents of [08_04_2026_modsWithID.txt](08_04_2026_modsWithID.txt)
```
"mod=843425103;843577117;450814997;1661066023;893339590;893349825;893328083;843593391;925018569;1808723766;2021778690;561177050;3023395342;623475643;1978434625;463939057;2011658088;2867537125;2060770170;1251859358;861133494;1804716719;2991684121;2467589125;950889473;2262255106;2095827925;1573550621;570118882;1397683809;3702543954;3065314104;893346105;843632231;1135541175;1515851169;1515845502;1673456286;2020940806;751965892;1623498241;498740884;766491311;866772689;1224892496;3055118909;1911374016;2522638637;1355571744;1779063631;2836999643;2198339170;2387297579;2291129343;2789152015;3032643455;2572487482;2735613231;2918542818;632435682;782415569;1841047025;3346427969;2699465073;3443045523;2791403093;1889104923;2447965207;2853202785;2231150238;1770265310;2595680138;2794721649;820924072;1354112941;2134489854"
```
