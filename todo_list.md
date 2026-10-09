# kksongs import — todo list (skipped & failed songs)

Source: whole-site dry-run of `python3 -m slokabase.plugins.kksongs`
(1,434 enumerated songs; 1,363 parsed OK / 9,902 verses — see
`/tmp/opencode/kk_dryrun.log` + `/tmp/opencode/kk_repass.log`).
DB: `database/slokabase.db`. Nothing here has been downloaded:
skipped songs cost zero HTTP requests (matched from index pages first).

## Failed (0)

No failures. 58 transient dry-run failures (unnumbered-verse pages,
drop-cap headers) were all fixed in the parser and recovered in the
re-pass — 57 parsed, 1 legitimately skipped (below).

## Skipped — already in database (70, zero downloads)

| # | Song (index title) | URL | Reason not downloaded |
|---|--------------------|-----|-----------------------|
| 1 | Adharam Madhuram | http://kksongs.org/songs/a/adharammadhuram.html | URL already in SongIndex.other_links |
| 2 | Akrodha Paramananda Nityananda Ray | http://kksongs.org/songs/a/akrodhaparamananda.html | URL already in SongIndex.other_links |
| 3 | Amar Jivan | http://kksongs.org/songs/a/amarjivan.html | URL already in SongIndex.other_links |
| 4 | Ami Jamuna Puline | http://kksongs.org/songs/a/amijamunapuline.html | URL already in SongIndex.other_links |
| 5 | Antara Mandire Jago Jago | http://kksongs.org/songs/a/antaramandire.html | URL already in SongIndex.other_links |
| 6 | Ar Koto Kal | http://kksongs.org/songs/a/arkotokal.html | URL already in SongIndex.other_links |
| 7 | Bhaja Bhakata Vatsala Sri Gaurahari (Sri Bhoga Arotik) | http://kksongs.org/songs/b/bhajabhakata.html | URL already in SongIndex.other_links |
| 8 | Bhaja Hu Re Mana | http://kksongs.org/songs/b/bhajahuremana.html | URL already in SongIndex.other_links |
| 9 | Boro Sukher Khabor Gai | http://kksongs.org/songs/b/borosukherkhabor.html | URL already in SongIndex.other_links |
| 10 | Ceto Darpana Marjanam (Sri Siksastakam) | http://kksongs.org/songs/c/cetodarpana.html | URL already in SongIndex.other_links |
| 11 | Ei Baro Karuna Koro Vaisnava Gosai | http://kksongs.org/songs/e/eibarokarunakoro.html | URL already in SongIndex.other_links |
| 12 | Emona Durmati | http://kksongs.org/songs/e/emonadurmati.html | URL already in SongIndex.other_links |
| 13 | Gauranga Bolite Habe Pulaka Sarira | http://kksongs.org/songs/g/gaurangabolite.html | URL already in SongIndex.other_links |
| 14 | Gauranga Koruna Koro | http://kksongs.org/songs/g/gaurangakorunakoro.html | URL already in SongIndex.other_links |
| 15 | Gauranger Duti Pada | http://kksongs.org/songs/g/gaurangeradutipada.html | URL already in SongIndex.other_links |
| 16 | Gay Gora Madhura Sware | http://kksongs.org/songs/g/gaygoramadhur.html | URL already in SongIndex.other_links |
| 17 | Gopinath! Mama Nivedana Suno | http://kksongs.org/songs/g/gopinatha1.html | URL already in SongIndex.other_links |
| 18 | Gopinath! Ghucao Samsara Jwala | http://kksongs.org/songs/g/gopinatha2.html | URL already in SongIndex.other_links |
| 19 | Gurudeva! Krpa Bindu Diya | http://kksongs.org/songs/g/gurudeva4.html | URL already in SongIndex.other_links |
| 20 | Hari Haraye Namah Krsna Yadavaya Namah | http://kksongs.org/songs/h/hariharayenamah.html | URL already in SongIndex.other_links |
| 21 | Hari Hari Biphale Janama Gonainu | http://kksongs.org/songs/h/harihari04a.html | URL already in SongIndex.other_links |
| 22 | Hari He Doyal Mora | http://kksongs.org/songs/h/harihedoyal.html | URL already in SongIndex.other_links |
| 23 | Hari Tum Haro Jana Ki Pir | http://kksongs.org/songs/h/haritumharo.html | URL already in SongIndex.other_links |
| 24 | He Govinda He Gopala He Dayala Lala | http://kksongs.org/songs/h/hegovindahegopal1.html | URL already in SongIndex.other_links |
| 25 | He Govinda He Gopala Kesava Madhava Dina Doyal | http://kksongs.org/songs/h/hegovindahegopal3.html | URL already in SongIndex.other_links |
| 26 | Jaya Jaya Gauracander Aratiko Sobha (Sri Gaura Arotik) | http://kksongs.org/songs/j/jayajayagoracander.html | URL already in SongIndex.other_links |
| 27 | Jaya Madhava Madana Murari | http://kksongs.org/songs/j/jayamadhavamadana.html | URL already in SongIndex.other_links |
| 28 | Jaya Radha Giri Vara Dhari | http://kksongs.org/songs/j/jayaradhagirivara.html | URL already in SongIndex.other_links |
| 29 | Jaya Radha Madhava | http://kksongs.org/songs/j/jayaradhamadhava.html | URL already in SongIndex.other_links |
| 30 | Jaya Radhe Jaya Krsna Jaya Vrndavana (I) | http://kksongs.org/songs/j/jayaradhejayakrsna.html | URL already in SongIndex.other_links |
| 31 | Jaya Radhe Jaya Krsna Jaya Vrndavana (I) | http://kksongs.org/songs/j/jayaradhejayakrsnajayavrndavana2.html | Title matches 'Jaya Radhe Jaya Krsna Jaya Vrndavana (I)' in SongIndex |
| 32 | Jaya Radhe Jaya Krsna Jaya Vrndavana (III) | http://kksongs.org/songs/j/jayaradhejayakrsnajayavrndavana3.html | URL already in SongIndex.other_links |
| 33 | Je Anilo Prema Dhana Karuna Pracura | http://kksongs.org/songs/j/jeanilopremadhana.html | URL already in SongIndex.other_links |
| 34 | Jiva Jago Jiva Jago | http://kksongs.org/songs/j/jivjago.html | URL already in SongIndex.other_links |
| 35 | Kabe Gaura Vane | http://kksongs.org/songs/k/kabegauravane.html | URL already in SongIndex.other_links |
| 36 | Kabe Ha’be Bolo | http://kksongs.org/songs/k/kabehabebolo.html | URL already in SongIndex.other_links |
| 37 | Krsna Hoite Caturmukha | http://kksongs.org/songs/k/krsnahoitecatur.html | URL already in SongIndex.other_links |
| 38 | Krsnotkirtana Gana Nartana (Sri Sadgosvamyastakam) | http://kksongs.org/songs/k/krsnotkirtana.html | URL already in SongIndex.other_links |
| 39 | Kunkumakta Kancanabja Garva (Sri Sri Radhikastakam) | http://kksongs.org/songs/k/kunkumaktakancanabja.html | URL already in SongIndex.other_links |
| 40 | Maine Ratana Lagai Radha Namaki | http://kksongs.org/songs/m/maineratanalagai.html | URL already in SongIndex.other_links |
| 41 | Mama Mana Mandire Raha Nisi-din | http://kksongs.org/songs/m/mamamanamandire.html | URL already in SongIndex.other_links |
| 42 | Manasa Deho Geho | http://kksongs.org/songs/m/manasadeho.html | URL already in SongIndex.other_links |
| 43 | Murali Manohara Gopala | http://kksongs.org/songs/m/muralimanoharagopala.html | URL already in SongIndex.other_links |
| 44 | Namamisvaram Saccidananda Rupam (Sri Damodarastakam) | http://kksongs.org/songs/n/namamisvaram.html | URL already in SongIndex.other_links |
| 45 | Namaste Narasimhaya (Sri Nrsimha Pranama) | http://kksongs.org/songs/n/namastenarasimha.html | URL already in SongIndex.other_links |
| 46 | Namo Namah Tulasi Krsna Preyasi (I) | http://kksongs.org/songs/n/namonamahtulasikrsna.html | URL already in SongIndex.other_links |
| 47 | Namo Namah Tulasi Krsna Preyasi | http://kksongs.org/songs/n/namonamahtulasikrsna2.html | Title matches 'Namo Namah Tulasi Krsna Preyasi' in SongIndex |
| 48 | Namo Namah Tulasi Maharani (Sri Tulasi Arotik) | http://kksongs.org/songs/n/namonamahtulasimaharani.html | URL already in SongIndex.other_links |
| 49 | Narada Muni Bajay Vina | http://kksongs.org/songs/n/naradamuni.html | URL already in SongIndex.other_links |
| 50 | Nitai Pada Kamala | http://kksongs.org/songs/n/nitaipadakamala.html | URL already in SongIndex.other_links |
| 51 | Ohe! Vaisnava Thakura Doyara Sagara | http://kksongs.org/songs/o/ohevaisnava.html | URL already in SongIndex.other_links |
| 52 | Om Purnamadah Purnamidam | http://kksongs.org/songs/o/ompurnamadahpurnam.html | Title matches 'Om Purnamadah Purnamidam' in SongIndex |
| 53 | Pralaya Payodhi Jale (Sri Dasavatara Stotra) | http://kksongs.org/songs/p/pralayapayodhijale.html | URL already in SongIndex.other_links |
| 54 | Sabse Unchi Prem Sagai | http://kksongs.org/songs/s/sabseoonchi.html | URL already in SongIndex.other_links |
| 55 | Samsara Davanala Lidha Loka (Sri Gurvastakam) | http://kksongs.org/songs/s/samsaradavanala.html | URL already in SongIndex.other_links |
| 56 | Sri Guru Carana Padma Kevala Bhakati Sadma (Sri Guru Puja) | http://kksongs.org/songs/s/srigurucaranapadma.html | URL already in SongIndex.other_links |
| 57 | Sri Krsna Caitanya Prabhu Doya Koro More | http://kksongs.org/songs/s/srikrsnacaitanyaprabhu.html | URL already in SongIndex.other_links |
| 58 | Sri Rupa Manjari Pada Sei Mora Sampada | http://kksongs.org/songs/s/srirupamanjaripada.html | URL already in SongIndex.other_links |
| 59 | Srita Kamala Kuca | http://kksongs.org/songs/s/sritakamala.html | URL already in SongIndex.other_links |
| 60 | Suddha Bhakata Carana Renu | http://kksongs.org/songs/s/suddhabhakata.html | URL already in SongIndex.other_links |
| 61 | Sujanarvuda Radhita Pada Yugam | http://kksongs.org/songs/s/sujanarvudaradhitapada.html | URL already in SongIndex.other_links |
| 62 | Sulabho Bhakti Yuktanam | http://kksongs.org/songs/s/sulabhobhaktiyuktanam.html | URL already in SongIndex.other_links |
| 63 | Sundara Mora Mana Kisora | http://kksongs.org/songs/s/sundaramor.html | URL already in SongIndex.other_links |
| 64 | Tum Meri Rakho Laja Hari | http://kksongs.org/songs/t/tummerirakholajahari.html | URL already in SongIndex.other_links |
| 65 | Udilo Aruna (Arunodaya Kirtana) | http://kksongs.org/songs/u/udiloaruna.html | URL already in SongIndex.other_links |
| 66 | Vamsidhari Krsna Murari | http://kksongs.org/songs/v/vamsidharikrsna.html | URL already in SongIndex.other_links |
| 67 | Vibhavari Sesa Aloka Pravesa | http://kksongs.org/songs/v/vibhavarisesa.html | URL already in SongIndex.other_links |
| 68 | Vidyara Vilase Katainu Kala | http://kksongs.org/songs/v/vidyaravilasekatainukala.html | URL already in SongIndex.other_links |
| 69 | Vrndavana Ramya Sthana | http://kksongs.org/songs/v/vrndavanaramya.html | URL already in SongIndex.other_links |
| 70 | Yasomati Nandana | http://kksongs.org/songs/y/yasomatinandana.html | URL already in SongIndex.other_links |

## Skipped — no lyrics on page (1, downloaded once to confirm)

| # | Song | URL | Reason not imported |
|---|------|-----|---------------------|
| 1 | Brahmadayah Suragana (Nrsimha Stuti, Bhagavata excerpt) | http://kksongs.org/songs/b/brahmadayahsuragana.html | Translation-only page: has TRANSLATION but no LYRICS verses, so no importable verse rows |

## Notes

- Old TODO_list slugs (`gopinath1`, `bhajabhakatavatsala`, `borosukherkhaborgai`,
  `srigurucaranapadmakevala`, …) are renamed pages already in the DB under
  current slugs (rows 7, 9, 17, 56 above) — no action needed.
- Orphan synonym files under those old names (e.g.
  `/synonym/b/bhajabhakatavatsala.html`) belong to the renamed songs, which
  are already imported; their word-meanings were not backfilled.
- ✅ IMPORT COMPLETED: `done: inserted=1363 skipped=71 failed=0`
  (DB: 292 → 1,655 songs, 2,687 → 12,895 verses; backup at
  `/tmp/opencode/slokabase.db.pre-kksongs.bak`). Took ~5 min — dry-run
  cache eliminated re-downloads. Integrity: no dup names/shorts, no
  orphans, no count mismatches; verified via Flask app
  (`/lib/293`, `/lib/1364`, `/admin/kksongs` all HTTP 200).
