# TIL (Today I Learned)

## 11주차

### 주제: 당근마켓 클론 코딩 프로젝트

#### 학습 내용
- 프로젝트 생성 및 초기 설정
- 앱 테마 설정 & 시작하기 기능 만들기

#### 내용
- 플러터 프로젝트 생성 (사용할 디렉토리로 먼저 이동)

```
flutter create 프로젝트명
```

- 기본 프로젝트 프레임 잡기, 자신이 사용할 프로젝트 폴더 구조를 설정

- 프로젝트 초기 라이브러리 (flutter_svg, google_fonts, equatable 설치)

#### 앱 테마 설정
```
@override
Widget build(BuildContext context) {
    return GetMaterialApp(
        title: '당근마켓 클론 코딩',
        initialRoute: '/',
        theme: ThemeData(
            appBarTheme: const AppBarTheme(
                elevation: 0,
                color: Color(0xff212123),
                titleTextStyle: TextStyle(
                    color: Colors.white,
                ),
            ),
            scaffoldBackGroundColor: const Color(0xff212123),
        ),
        getPages: [
            GetPage(name: '/', page : () => const App()),
        ],
    ),
}
```
- 위와 같이 설정 시 화면의 색이 어두운 계열로 변경됨

#### 첫 페이지 진입 처리
- shared_preferences를 사용해 사용자가 앱을 처음 실행했는지 확인하게 함
```
flutter pub add shared_preferences
```

#### 시작하기 기능 만들기
- app.dart에서 업데이트 처리 시, 상태 변경을 setState로 처리하여 바로 SplashPage로 변경할 수 있음

- 이를 위해 initStartPage 위젯에 onStart라는 이벤트를 부모로부터 설정할 수 있게 하여, app.dart에서 업데이트를 처리하게 함.

- app.dart
```
@override
Widget build(BuildContext context) {
    return isInitStarted ? InitStartPage (
        onStart: () {
            setState(() {
                isInitStarted = false;
            });
            prefs.setBool('isInitStarted', isInitStarted);
        },
    )
    : const SplashPage();
}
```

```
// import 생략

class InitStartPage extends StatelessWidget {
    final Function() onStart;
    const InitStartPage({super.key, required this.onStart});

    @override
    Widget build(buildContext context) {
        return Scaffold(
            body: Center(
                // 생략
            ),
            bottomNavigationBar : Padding(
                padding: EdgeInsets.only(
                    left:25, right:25, bottom: 25 + Get.mediaQuery.padding.bottom),
                child: Btn(
                    onTap: onStart,
                    child: const AppFont(
                        '시작하기',
                        align : TextAlign.center,
                        size: 18,
                        fontWeight: FontWeight.bold,
                    ),
                ),
            ),
        );
    }
}
```
---

## 12주차

### 주제: 당근마켓 클론 코딩 프로젝트

#### 학습 내용
- 스플래시 페이지
- 앱 Root 레이아웃 구성

#### 스플래시 페이지의 목적
- 스플래시 페이지는 앱이 실행될 때 필요한 정보를 불러오거나, 서버 데이터와 로컬 데이터의 싱크를 맞추는 상황에서 용이함

- 이는 사용자에게 지루함을 주지 않기 위해 정보를 보여주거나, 앱이 어떤 상황이라는 것을 인식시켜주는 역할을 함

#### 코드 예시
- 스플레시 페이지에서 진행 상황을 안내하기 위해 splash/controller 에서 splash_controller.dart 생성

```
class SplashController extends GetxController {
    Rx<StepType> loadStep = StepType.dataLoad.obs;

    changeStep(StepType type) {
        loadStep(type);
    }
}
```

- splash.dart 파일에서 splash_controller.dart 사용

```
// import 생략

class SplashPage extends GetView<SplashController> {
    const SplashPage({super.key});

    @override
    Widget build(BuildContext context) {
        return Scaffold(
            body: Center(
                child: 0bx(
                    () => Text(
                        '${controller.loadStep.value.name}중 입니다.',
                        style: const TextStyle(color: Colors.white),
                    ),
                ),
            ),
        );
    }
}
```
#### 앱 Root 레이아웃 구성
- 플러터 어플리케이션의 Root 레이아웃을 구성하는 방법을 배움

- BottomNavigationBar를 사용하여 하단 네비게이션 메뉴를 생성 후, 메뉴를 클릭할 때마다 페이지가 바뀌도록 설정

- 그 후 root.dart 파일을 생성하여 Scaffold 위젯으로 기본 레이아웃을 설정하고 BottomNavigationBar로 하단 메뉴의 상태를 관리

- TabBarView로 각 메뉴에 맞는 페이지를 연결하였음

---

## 13주차

### 주제: 당근마켓 클론 코딩 프로젝트

#### 학습 내용
- 홈 화면 구성

#### 핵심 개념
- 홈 화면 구성의 3가지
- 헤더(Appbar), 보디(ListView), 레이어 버튼(FloatingActionButton)

#### 헤더 구성
- home_page.dart 파일의 Scaffold appBar 옵션
```
appBar: AppBar(
    leadingWidth: Get.width * 0.6,
    leading: Padding(
        padding: const EdgeInsets.only(left: 25),
        child: Row(children : [
            const AppFont(
                '아라동',
                fontWeight: FontWeight.bold,
                size: 20,
                color: Colors.white,
            ),
            const SizedBox(width: 10),
            SvgPicture.asset('assets/svg/icons/bottom_arrow.svg'),
        ]),
    ),
),
// 우측 actions 부분 생략
```

#### 보디 구성
- 상품들 사이의 회색 선 구분을 위해 ListView.separated 위젯 사용

```
class _ProductList extends StatelessWidget {
    const _ProductList({super.key});

    Widget Build(BuildContext context) {
        return ListView.seperated(
            padding: const EdgeInsets.only(left: 25, right: 25, top: 20),
            itemBuilder: (context, index) {
                return Container(
                    height: 100,
                    color: Colors.blue,
                );
            },
            seperatorBuilder: (context, index) => const Padding(
                padding : EdgeInsets.symmetric(vertical: 10.0),
                child: Divider(
                    color: Color(0xff3C3C3E),
                ),
            ),
            itemCount: 10,
        );
    }
}
```

- 위의 코드를 실행 시 영역을 구분하여 레이어가 표시됨 (아직 사진을 넣지 않아 파란색 박스로 뜸)

- _ProductList 클래스 내의 _productOne 위젯 함수
```
Widget _productOne(int index) {
    return Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
            ClipRRect (
                borderRadius: BorderRaidus.circular(7),
                child: SizedBox(
                    width: 100,
                    height: 100,
                    child : Image.network(
                        'http://cdn.kgmaeil.net/news/photo/202007/245825_49825_2217.jpg',
                        fit: BoxFit.cover,
                    ),
                ),
            ),
            const SizedBox(width: 15),
            Expanded(
                child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                        const SizedBox(height: 10),
                        AppFont(
                            'Yaamj 상품 $index 무료로 드려요 :)',
                            color: Colors.white,
                            size: 16,
                        ),
                        const SizedBox(height: 5),
                        const AppFont(
                            '개발하는남자 2023 07 08',
                            color: Color(0xff878B93),
                            size:12,
                        ),
                        const SizedBox(height: 5),
                        const Row(
                            children: [
                                Appfont(
                                    '나눔',
                                    size: 14,
                                    fontWeight: FontWeight.bold,
                                ),
                                AppFont(
                                    '?', size: 16,
                                ),
                            ],
                        )
                    ],
                ),
            )
        ],
    );
}
```

- 후에 레이어 버튼 구성만 하면 홈 화면 구성은 완성이다
---
