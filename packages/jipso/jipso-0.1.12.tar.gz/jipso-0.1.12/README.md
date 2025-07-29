<div style="text-align: center;">
  <img width="300" src="https://cdn.jipso.org/logo/jipso_framework.svg" alt="JIPSO Framework Logo"/>
</div>


<p align="center">
  <a href="https://codecov.io/gh/jipso-foundation/jipso-py">
    <img src="https://codecov.io/gh/jipso-foundation/jipso-py/branch/main/graph/badge.svg" alt="Codecov"/>
  </a>
  <a href="https://badge.fury.io/py/jipso">
    <img src="https://badge.fury.io/py/jipso.svg" alt="PyPI version"/>
  </a>
  <a href="https://hub.docker.com/r/jipsofoundation/jipso">
    <img src="https://img.shields.io/docker/pulls/jipsofoundation/jipso" alt="Docker Pulls"/>
  </a>
  <a href="https://jipso-py.readthedocs.io/en/latest/">
    <img src="https://readthedocs.org/projects/jipso-py/badge/?version=latest" alt="Documentation Status"/>
  </a>
  <a href="https://doi.org/10.5281/zenodo.1234567">
    <img src="https://zenodo.org/badge/DOI/10.5281/zenodo.1234567.svg" alt="DOI"/>
  </a>
  <a href="https://app.fossa.com/projects/git%2Bgithub.com%2Fjipso-foundation%2Fjipso-py?ref=badge_shield">
    <img src="https://app.fossa.com/api/projects/git%2Bgithub.com%2Fjipso-foundation%2Fjipso-py.svg?type=shield" alt="FOSSA Status"/>
  </a>
</p>

## 🚀 QUICK START

```bash
pip install jipso
```

```python
import jipso

prompt1 = 'Write leave request email'
prompt2 = 'Write formal leave request email with clear reason and timeline'
result = jipso.pvp(prompt1, prompt2, judgement='chatgpt-4o')
print(result)
```

## 🧭 ROADMAP

The library currently only introduces concepts and abstract classes. JIPSO Foundation needs to work with **AI platforms** to innovate APIs in the JIPSO style, and requires funding to maintain the library.

Library Development Roadmap:
- 👉 v0.1: Establish CI/CD pipeline
- [ ] v0.2: JIPSO Foundation drafts abstract classes
- [ ] v0.3: JIPSO Foundation aligns with AI developers on abstract classes
- [ ] v0.4: Open for community contributions to build abstract classes
- [ ] v1.0: Alpha release with new APIs
- [ ] v1.1: Beta release with new APIs
- [ ] v1.2: Open for community contributions to development

**⚠️ Local AI Limitation**: The current Docker release does not support local AI providers (Ollama, HuggingFace) due to dependency overhead - local AI packages increase image size from ~300MB to ~4.5GB and require 16-32GB RAM. **JIPSO Foundation is actively collaborating with AI platform vendors** to develop lightweight client SDKs and hybrid deployment architectures. For immediate local AI needs, use development installation (`pip install jipso[local]`) or Docker Compose with separate inference containers.

## 👥 COMMUNITY DISCUSSION AND CONTRIBUTION (PLANNING)

### JIPSO Community Proposal
**JCP (JIPSO Community Proposal)** is a design document that provides information to the JIPSO community or describes a new feature, process, or enhancement for the JIPSO Framework. Similar to Python's PEP or LangChain's RFC, JCPs serve as the primary mechanism for proposing major changes, collecting community input, and documenting design decisions.

JCPs differ from traditional RFCs through their domain-expertise consensus model - admins from channels with the same technical specialty across different language regions must reach consensus (e.g., Privacy experts from English, Chinese, Russian, Indian, and Vietnamese channels collaborate; Enterprise specialists across all regions coordinate; Technical architecture experts form cross-language working groups). This ensures domain expertise alignment while maintaining global technical consistency, eliminating the need for full cross-domain consensus between unrelated specializations.

### Education Community (Microsoft Teams)
| Community | Admin |
|--|--|
[🇬🇧 JIPSO Education Global](https://teams.live.com/l/community/FEA2r9tFxkode6yegE) | vacancy |
[🇨🇳 JIPSO Education 中国](https://teams.live.com/l/community/FEA3iZADI16JNJ01gI) | vacancy |
[🇷🇺 JIPSO Education Россия](https://teams.live.com/l/community/FEA8Kbpi0O42WF1WgI) | vacancy |
[🇮🇳 JIPSO Education भारत](https://teams.live.com/l/community/FEAqZ2DW6oEYBMnYgI) | vacancy |
[🇻🇳 JIPSO Education Việt Nam](https://teams.live.com/l/community/FEANIvvgtmficCm6wE) | vacancy |
[Youtube]() | vacancy |
[Tiktok: @jipso.foundation](https://www.tiktok.com/@jipso.foundation) | vacancy |

### AI Developer Community (Discord)
| Community | Admin |
|--|--|
[🇬🇧 #ai-developer-community](https://discord.gg/vbBe8W5jqW) | vacancy |
[🇨🇳 #ai框架开发者社区](https://discord.gg/evCQQMF7Xd) | vacancy |
[🇷🇺 #разработчики-ai-фреймворков](https://discord.gg/eUBPHQsEAZN) | vacancy |
[🇮🇳 #ai-framework-विकासकर्ता](https://discord.gg/hDhnqw5TVn) | vacancy |
[🇩🇪 #ai-framework-entwickler](https://discord.gg/HcQvxqYpuZ) | vacancy |
[🇫🇷 #développeurs-framework-ia](https://discord.gg/BnhNNHNJC2) | vacancy |
[🇯🇵 #aiフレームワーク開発者](https://discord.gg/gYuAJBzBZf) | vacancy |
[🇰🇷 #ai프레임워크-개발자](https://discord.gg/yCkVfzKxg8) | vacancy |
[🇻🇳 #nhà-sáng-phát-triển-ai](https://discord.gg/jXXwFmgXrF) | vacancy |


### Content Creator Community (Discord)
| Community | Admin |
|--|--|
[🇬🇧 #content-creator-community](https://discord.gg/PUVcnMQnFx) | vacancy |
[🇨🇳 #内容创作者社区](https://discord.gg/kjpfv5SVp6) | vacancy |
[🇷🇺 #сообщество-контент-криэйторов](https://discord.gg/yuWuMVemVC) | vacancy |
[🇮🇳 #सामग्री-निर्माता-समुदाय](https://discord.gg/u8QmExRdCA) | vacancy |
[🇩🇪 #content-creator-gemeinschaft](https://discord.gg/PG8N8NpECY) | vacancy |
[🇫🇷 #communauté-créateurs-de-contenu](https://discord.gg/NR9DrDeU22) | vacancy |
[🇯🇵 #コンテンツ制作者コミュニティ](https://discord.gg/FdaWFtbzX5) | vacancy |
[🇰🇷 #콘텐츠-창작자-커뮤니티](https://discord.gg/8jtwVykkMC) | vacancy |
[🇻🇳 #nhà-sáng-tạo-nội-dung-số](https://discord.gg/yH7kZwPX4M) | vacancy |

### Game Text Based Community (Discord)
| Community | Admin |
|--|--|
[🇬🇧 #game-text-based-community](https://discord.gg/35gsJgjHNc) | vacancy |
[🇨🇳 #文字冒险游戏开发者](https://discord.gg/AZssCCP3mD) | vacancy |
[🇷🇺 #разработчики-текстовых-игр](https://discord.gg/9YXQFUjcB2) | vacancy |
[🇮🇳 #पाठ-आधारित-गेम-डेवलपर](https://discord.gg/e2TkzKRWu8) | vacancy |
[🇩🇪 #textbasierte-spieleentwickler](https://discord.gg/H42wAERmpv) | vacancy |
[🇫🇷 #développeurs-jeux-textuels](https://discord.gg/MB44uty7v2) | vacancy |
[🇯🇵 #テキストゲーム開発者](https://discord.gg/aYP2u2nYXU) | vacancy |
[🇰🇷 #텍스트-게임-개발자](https://discord.gg/84jYADk2HR) | vacancy |
[🇻🇳 #nhà-phát-triển-game-dạng-văn-bản](https://discord.gg/s3JzwFQcZZ) | vacancy |

### Social Community
| Community | Admin |
|--|--|
[Facebook]() | vacancy |
[X: jipsofoundation](https://x.com/jipsofoundation) | vacancy |
[Instagram: jipso_foundation](http://instagram.com/jipso_foundation) | vacancy |
[Threads: @jipso_foundation](https://www.threads.com/@jipso_foundation) | vacancy |

### Announcements Channel
- [🇬🇧 Slack]()
- [🇨🇳 DingTalk]()
- [🇷🇺 Telegram]()
- [🇮🇳 WhatsApp]()
- [🇻🇳 Zalo]()

### Official Contact
- [🌐 Website: jipso.org](https://jipso.org)
- [📬 Email: contact@jipso.org](mailto:contact@jipso.org)
- [🐛 #bug-reports](https://discord.gg/pb8aAMJG6t)

## 💰 SPONSORSHIP
This project has received no external funding, sponsorship, or investment. All development is fully volunteer-based at this stage.
