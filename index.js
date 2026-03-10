import { useRouter } from "expo-router";
import { useState } from "react";
import { StyleSheet, Text, TouchableOpacity, View } from "react-native";

export default function HomeScreen() {
  const [step, setStep] = useState(1);
  const router = useRouter();

  // 온보딩 화면만 표시
  return (
    <View style={styles.container}>
      <Text style={styles.emoji}>
        {step === 1 ? "🍳" : step === 2 ? "✨" : "🎉"}
      </Text>

      {step === 1 && (
        <>
          <Text style={styles.title}>홍길동에 오신 걸 환영합니다! 👋</Text>
          <Text style={styles.subtitle}>
            냉장고 속 재료로 맛있는 레시피를 추천해드립니다.
          </Text>
        </>
      )}

      {step === 2 && (
        <>
          <Text style={styles.title}>간단한 3가지 단계 📱</Text>
          <Text style={styles.subtitle}>
            1. 냉장고 사진 촬영{"\n"}2. AI가 재료 인식{"\n"}3. 맞춤 레시피 추천
          </Text>
        </>
      )}

      {step === 3 && (
        <>
          <Text style={styles.title}>지금 시작하세요! 🚀</Text>
          <Text style={styles.subtitle}>
            냉장고를 촬영하고 맛있는 요리를 만들어보세요!
          </Text>
        </>
      )}

      <View style={styles.progressContainer}>
        <View
          style={[styles.progressDot, step >= 1 && styles.progressDotActive]}
        />
        <View
          style={[styles.progressDot, step >= 2 && styles.progressDotActive]}
        />
        <View
          style={[styles.progressDot, step >= 3 && styles.progressDotActive]}
        />
      </View>

      <View style={styles.buttonContainer}>
        {step > 1 && (
          <TouchableOpacity
            style={styles.prevButton}
            onPress={() => setStep(step - 1)}
          >
            <Text style={styles.buttonText}>이전</Text>
          </TouchableOpacity>
        )}

        {step < 3 ? (
          <TouchableOpacity
            style={[styles.button, { flex: 1 }]}
            onPress={() => setStep(step + 1)}
          >
            <Text style={styles.buttonText}>다음</Text>
          </TouchableOpacity>
        ) : (
          <TouchableOpacity
            style={[styles.startButton, { flex: 1 }]}
            onPress={() => router.push("/(tabs)/main")}
          >
            <Text style={styles.buttonText}>시작하기 📸</Text>
          </TouchableOpacity>
        )}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center",
    paddingHorizontal: 20,
    paddingBottom: 40,
  },
  emoji: {
    fontSize: 80,
    marginBottom: 20,
  },
  welcomeText: {
    fontSize: 32,
    fontWeight: "bold",
    color: "#333",
    marginBottom: 10,
  },
  title: {
    fontSize: 24,
    fontWeight: "bold",
    color: "#333",
    textAlign: "center",
    marginBottom: 15,
  },
  subtitle: {
    fontSize: 16,
    color: "#666",
    textAlign: "center",
    marginBottom: 40,
    lineHeight: 24,
  },
  progressContainer: {
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
    marginBottom: 40,
    gap: 10,
  },
  progressDot: {
    width: 10,
    height: 10,
    borderRadius: 5,
    backgroundColor: "#ddd",
  },
  progressDotActive: {
    backgroundColor: "#FFD700",
  },
  buttonContainer: {
    flexDirection: "row",
    gap: 10,
    width: "100%",
  },
  button: {
    backgroundColor: "#FFD700",
    paddingHorizontal: 20,
    paddingVertical: 15,
    borderRadius: 25,
    justifyContent: "center",
    alignItems: "center",
  },
  prevButton: {
    backgroundColor: "#ddd",
    paddingHorizontal: 20,
    paddingVertical: 15,
    borderRadius: 25,
    justifyContent: "center",
    alignItems: "center",
    minWidth: 60,
  },
  startButton: {
    backgroundColor: "#FF6B9D",
    paddingHorizontal: 20,
    paddingVertical: 15,
    borderRadius: 25,
    justifyContent: "center",
    alignItems: "center",
  },
  buttonText: {
    fontSize: 16,
    fontWeight: "bold",
    color: "#fff",
    textAlign: "center",
  },
});
