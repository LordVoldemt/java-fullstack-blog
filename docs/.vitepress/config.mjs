const repositoryName = process.env.GITHUB_REPOSITORY?.split("/")[1];
const isProjectPagesRepo =
  Boolean(repositoryName) && !repositoryName.endsWith(".github.io");
const base =
  process.env.GITHUB_ACTIONS && isProjectPagesRepo
    ? `/${repositoryName}/`
    : "/";

const javaSidebar = [
  {
    text: "Java 后端基础",
    items: [
      { text: "栏目总览", link: "/java/" },
      { text: "Java 基础", link: "/java/basics/java-basics-overview" },
      { text: "Java 集合", link: "/java/collections/java-collections-overview" },
      { text: "Java 并发编程", link: "/java/concurrency/java-concurrency-overview" },
      { text: "JVM", link: "/java/jvm/jvm-overview" },
      { text: "Spring", link: "/java/spring/spring-overview" },
      { text: "Spring Boot", link: "/java/spring-boot/spring-boot-overview" },
      { text: "数据库与 MySQL", link: "/java/mysql/mysql-overview" },
      { text: "Maven / Gradle", link: "/java/build-tools/maven-gradle-overview" },
      { text: "Git 与开发工具", link: "/java/dev-tools/git-dev-tools-overview" }
    ]
  }
];

const microservicesSidebar = [
  {
    text: "微服务与中间件",
    items: [
      { text: "栏目总览", link: "/microservices/" },
      { text: "Redis", link: "/microservices/redis/redis-overview" },
      {
        text: "Spring Cloud Alibaba",
        link: "/microservices/spring-cloud-alibaba/spring-cloud-alibaba-overview"
      }
    ]
  }
];

const aiSidebar = [
  {
    text: "AI 与大模型",
    items: [
      { text: "栏目总览", link: "/ai/" },
      { text: "大模型基础", link: "/ai/llm-basics/llm-basics-overview" },
      { text: "AI 应用开发", link: "/ai/ai-app-dev/ai-app-dev-overview" }
    ]
  }
];

const vibeCodingSidebar = [
  {
    text: "Vibe Coding",
    items: [
      { text: "栏目总览", link: "/vibe-coding/" },
      { text: "Trae", link: "/vibe-coding/trae/trae-overview" },
      { text: "Codex", link: "/vibe-coding/codex/codex-overview" },
      { text: "Claude", link: "/vibe-coding/claude/claude-overview" },
      { text: "工作流总览", link: "/vibe-coding/workflows/vibe-coding-overview" }
    ]
  }
];

const projectSidebar = [
  {
    text: "项目实战",
    items: [
      { text: "栏目总览", link: "/project/" },
      { text: "Java 项目实战", link: "/project/java-projects/java-projects-overview" },
      { text: "AI 项目实战", link: "/project/ai-projects/ai-projects-overview" },
      { text: "博客搭建与部署总结", link: "/project/blog-build/blog-build-overview" }
    ]
  }
];

const careerSidebar = [
  {
    text: "面试与成长",
    items: [
      { text: "栏目总览", link: "/career/" },
      { text: "面试题与八股总结", link: "/career/interview/interview-overview" },
      { text: "学习路线与经验总结", link: "/career/learning-path/learning-path-overview" }
    ]
  }
];

export default {
  base,
  title: "java全栈",
  description: "一个聚焦 Java 后端、微服务、AI 应用与 Vibe Coding 的个人知识博客。",
  lang: "zh-CN",
  cleanUrls: true,
  lastUpdated: true,
  head: [
    ["meta", { name: "theme-color", content: "#0d5c63" }],
    [
      "meta",
      {
        name: "keywords",
        content: "Java, Spring Boot, MySQL, Redis, AI, 大模型, Vibe Coding, Codex, Claude, Trae"
      }
    ]
  ],
  themeConfig: {
    logo: "/favicon.svg",
    nav: [
      { text: "首页", link: "/" },
      { text: "Java 后端基础", link: "/java/" },
      { text: "微服务与中间件", link: "/microservices/" },
      { text: "AI 与大模型", link: "/ai/" },
      { text: "Vibe Coding", link: "/vibe-coding/" },
      { text: "项目实战", link: "/project/" },
      { text: "面试与成长", link: "/career/" },
      { text: "关于", link: "/about" }
    ],
    sidebar: {
      "/java/": javaSidebar,
      "/microservices/": microservicesSidebar,
      "/ai/": aiSidebar,
      "/vibe-coding/": vibeCodingSidebar,
      "/project/": projectSidebar,
      "/career/": careerSidebar
    },
    search: {
      provider: "local"
    },
    outline: {
      label: "文章目录",
      level: [2, 3]
    },
    docFooter: {
      prev: "上一篇",
      next: "下一篇"
    },
    returnToTopLabel: "回到顶部",
    sidebarMenuLabel: "栏目导航",
    darkModeSwitchLabel: "主题切换",
    lightModeSwitchTitle: "切换到浅色模式",
    darkModeSwitchTitle: "切换到深色模式",
    notFound: {
      title: "页面不存在",
      quote: "你访问的内容可能还在整理中，或者已经移动到新的栏目结构里。",
      linkLabel: "回到首页",
      linkText: "返回博客首页"
    },
    footer: {
      message: "持续记录 Java、AI 和工程实践。",
      copyright: "Copyright © 2026 java全栈"
    }
  }
};
