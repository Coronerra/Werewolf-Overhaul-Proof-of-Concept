# Source

Everything used to build the release. Python 3 (numpy, scipy, Pillow; py7zr only for packaging).
Scripts read original mod files from `input/` and write to `out/` (relative to where you run them).
You must supply `input/` yourself from your own downloads; no third-party files are included here.

## femwolf/ - werewolf bodies + main plugin
| File | Does |
|---|---|
| `nif.py` | minimal SSE NIF block reader/writer |
| `geo.py` | reads skinned BSTriShape geometry from NiSkinPartition (positions, UVs, normals, weights, triangles) |
| `shinfo.py` | shader / alpha property readers |
| `mkheadless.py` | ABC male: unlinks WereWolfHead/EyesLeft/EyesRight/Teeth so the MFA head part is used. `python mkheadless.py <ABC character assets dir> out/common/meshes/actors/werewolfbeast/character assets/coronerra` |
| `shell.py`, `mkfluffy.py` | fur shells: clones the body shapes 10x, pushed 0.44 units/layer along welded normals, same skin weights, alpha-test threshold 24..240, only where Fluffworks' own shell UV mask has fur (male sheath excluded). Builds male + female Default/2T/6T |
| `mkshelltex.py` | shell textures: blurred body diffuse RGB + Fluffworks shell alpha, uncompressed with mips |
| `validate.py` | checks every shape (skin, partitions, bone indices, finite positions, _0/_1 match) |
| `recs.py`, `dump.py`, `mkesl.py` | writes `FemaleWerewolf_ABC_HDT_MFA.esp` for every FOMOD option (`out/esp/{smooth,fluffy}_{Default,2T,6T}/`): ARMA NakedTorsoWerewolfBeast (body slots 32,33,34,37,38,40, head slot 30 off) + Growl/MFA merged DLC2WerebearBeastRace |

`input/` expected: `Monster Lip Sync/MonsterLipSync1.esp`, `Growl - Werebeasts of Skyrim/...esp`,
`BakaFactory Animated Beasts Cocks/...`, `MFA and Growl Patch/meshes/...` (from HDT Werewolves),
`HDT werewolves SMP/...` (female diffuse), `fluffworks/...` (Fluffworks werewolf body + shell texture).

## compat/ - JS Emissive Eyes compat patch
`mkdb.py` parses plugins in `input/` -> `db.pkl`; `mkpatch.py` writes `FemaleWerewolf_Compat_JSEyes.esp`
(JS Emissive Eyes SE - Growl race records + MFA head parts / FaceGen flag / head slot / voice).

## beastaware/ - Beast Aware
`mkesp.py` writes `BeastAware.esp`; Papyrus sources in `Scripts/Source/` (compile with Caprica or the CK
compiler, imports: vanilla + SKSE + SkyUI SDK + SkyrimNet API); SkyrimNet prompt bundle in `SkyrimNet/`.

## fomod/
`ModuleConfig.xml` / `info.xml` for the full Fur style (Smooth/Fluffy) x Female body (Default/2T/6T) installer.
**Only Fluffy + 2T was tested.** The release itself is a plain install of that one variant.
