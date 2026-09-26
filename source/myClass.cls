% mystyle.cls
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{myClass}

% 繼承自ctexart並設置默認選項
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{ctexart}}
\ProcessOptions\relax
\LoadClass[12pt]{ctexart}

% 加載所需宏包
\RequirePackage{lipsum}
\RequirePackage{fancyhdr}
\RequirePackage{lastpage}
\RequirePackage{titlesec}
\RequirePackage{geometry}
\RequirePackage{subfiles}
\RequirePackage{amsmath}
\RequirePackage{amsthm}
\RequirePackage{amssymb}
\RequirePackage{graphicx}
\RequirePackage{gensymb}
\RequirePackage{longtable}
\RequirePackage{algpseudocode}
\RequirePackage[linesnumbered,ruled,vlined]{algorithm2e}
\RequirePackage{inputenc}
\RequirePackage{listings}
\RequirePackage{float}
\RequirePackage{tocloft}
\RequirePackage{soul, color}
\RequirePackage{enumerate}
\RequirePackage{enumitem}
\RequirePackage[bookmarks=true, colorlinks, citecolor=blue, linkcolor=black]{hyperref}
\RequirePackage{xcolor}
\RequirePackage{appendix}
\RequirePackage{tikz}
\RequirePackage{minted}
\RequirePackage{tasks}
\usetikzlibrary{shapes.geometric, arrows, calc, positioning}

% 數學運算符定義
\DeclareMathOperator*{\argmax}{arg\,max}
\DeclareMathOperator*{\sgn}{sgn}

% 標題格式設定
\titleformat{\section}
  {\centering\normalfont\fontsize{22pt}{26pt}\bfseries}
  {第 \thesection 章}{1em}{}
  
\titleformat{\subsection}
  {\normalfont\fontsize{16pt}{20pt}\bfseries}
  {\thesubsection}{1em}{}
  
% 目錄間距
\setlength{\cftbeforesecskip}{1.5ex}

% 列表格式設定
\setlist[enumerate]{
  label=(\arabic*),    % 主級別：(1)
  itemsep=0pt,         % 條目間距
  parsep=0pt,          % 條目內段落間距
  topsep=0pt,          % 列表整體上下間距
  partopsep=0pt,       % 避免空行時的額外間距
}
\setlist[itemize]{
  itemsep=0pt,         % 條目間距
  parsep=0pt,          % 條目內段落間距
  topsep=0pt,          % 列表整體上下間距
  partopsep=0pt,       % 避免空行時的額外間距
}
% 段落間距
\setlength{\parskip}{0.3em}

% 頁面佈局
\geometry{a4paper,left=15mm, right=15mm, bottom=15mm, top=30mm}

% 頁眉頁腳設定
\pagestyle{fancy}
\fancyhf{}
\setlength{\headheight}{12.7pt}
\fancyhead[R]{濠江中學附屬英才學校圖靈隊總 \pageref{LastPage} 頁之第 \thepage 頁}

% 中文環境重定義
\renewcommand{\figurename}{圖}
% \renewcommand{\abstractname}{\fontsize{22pt}{100pt}\selectfont 摘要}
\renewcommand{\abstractname}{\selectfont 摘要}
\renewcommand{\contentsname}{\hfill\fontsize{26}{30}\selectfont\bfseries 目錄\hfill}

% 自定義定理環境
\newtheorem{assumption}{假設}
\newtheorem*{explanation}{解釋}