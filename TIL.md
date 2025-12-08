# TIL (Today I Learned)

## 11주차

### 주제: 당근마켓 클론 코딩 프로젝트

#### 학습 내용
- 프로젝트 설정
- 첫 페이지 진입

#### 플러터 프로젝트 생성
- cmd에서 프로젝트 생성하고 실행해보기

```
flutter create example
cd example
flutter run
```

#### assets 구성
- pubspec.yaml 파일에서 flutter 밑에 작성
```
assets:
    - assets/images/
    - assets/svg/
    - assets/svg/icons
```

#### 프로젝트 초기 라이브러리 설치
- get, flutter_svg, equtable, google_font를 설치할 예정, 터미널에 입력
```
flutter pub add get flutter_svg equatable google_fonts
```

#### GetX 라우트 설정
- Getx를 사용하여 라우팅을 관리하려면 GetMaterialApp위젯을 사용
- GetMaterialApp에 있는 getPages라는 옵션 파라미터를 이용하여 라우트 구성가능
  
#### 앱 테마 설정
- 어두운 계열의 화면으로 변경하려면
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

#### 첫 페이지 진입 처리
- shared_preferences를 사용해 앱이 실행된 지 확인
- 터미널에 입력하여 라이브러리 설치
```
flutter pub add shared_preferences
```

## 12주차

### 주제: 당근마켓 클론 코딩 프로젝트

#### 학습 내용
- 스플래시 페이지
- 앱 Root 레이아웃 구성

#### 스플래시 페이지
- 스플래시 페이지는 앱이 시작될 때 잠깐 보여주는 화면으로, 데이터를 로드하거나 인증 상태를 확인하는 동안 표시된다.
- 이는 서버 데이터와 로컬 데이터의 싱크를 맞추는 상황에서 사용되며 사용자에게 지루함을 주지 않기 위해 정보를 보여주거나, 앱이 어떤 상황인지 인식시켜주는 역할을 한다

#### SplashController 생성
-splash.controller.dart
```
class SplashController extends GetxController {
    Rx<StepType> loadStep = StepType.dataLoad.obs;

    changeStep(StepType type) {
        loadStep(type);
    }
}
```

#### 앱 Root 레이아웃 구성
- 먼저 NavigationBar를 사용해 하단에 내비게이션 메뉴를 만든다
- 메뉴를 클릭할 때 페이지가 변경되도록 설정한다
- 파일을 생성해 레이아웃을 성정하고 하단 메뉴의 상태를 관리한다
- TabBarView로 각 메뉴에 맞는 페이지를 연결한다 
