---
name: android-native
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Production-grade skill for native Android development with Jetpack Compose, MVVM, Hilt, Room, and Compose Navigation. Covers project setup, UI, architecture, DI, persistence, networking, and testing.
tags: [android, kotlin, jetpack-compose, mvvm, mobile, native]
trigger: When the user asks to create, refactor, fix, or explain native Android code, Jetpack Compose, MVVM, Hilt, Room, Retrofit, navigation, or Android testing.
min_version: "8.2"
---

# Android Native Skill

## Description

Comprehensive skill for building production-ready native Android applications using Kotlin, Jetpack Compose, and modern architecture components. Covers the full stack: UI with Compose, state management, MVVM with ViewModel and StateFlow, dependency injection with Hilt, local persistence with Room, networking with Retrofit, Compose Navigation, and testing.

## Table of Contents

1. [Project Setup](#1-project-setup)
2. [Jetpack Compose](#2-jetpack-compose)
3. [MVVM Architecture](#3-mvvm-architecture)
4. [Compose Navigation](#4-compose-navigation)
5. [Dependency Injection (Hilt)](#5-dependency-injection-hilt)
6. [Persistence (Room & DataStore)](#6-persistence-room--datastore)
7. [Networking (Retrofit & OkHttp)](#7-networking-retrofit--okhttp)
8. [Testing](#8-testing)
9. [Best Practices Checklist](#9-best-practices-checklist)
10. [Common Pitfalls](#10-common-pitfalls)
11. [References](#11-references)

## When to Invoke

- Creating or refactoring a native Android app with Jetpack Compose
- Setting up MVVM with ViewModel, StateFlow, and Repository pattern
- Implementing Compose Navigation with type-safe routes
- Configuring Hilt for dependency injection
- Creating Room entities, DAOs, and database
- Setting up Retrofit for REST API consumption
- Writing unit tests, integration tests, and Compose UI tests
- Handling state in Compose (remember, derivedStateOf, snapshotFlow)
- Implementing Material Design 3 theming and components

---

## 1. Project Setup

### Directory Layout

```
app/
  src/main/java/com/example/app/
    App.kt                    # @HiltAndroidApp Application class
    MainActivity.kt           # setContent { App() }
    di/
      AppModule.kt            # Hilt modules
      DatabaseModule.kt
      NetworkModule.kt
    ui/
      theme/
        Color.kt
        Type.kt
        Theme.kt
        Shape.kt
      screens/
        home/
          HomeScreen.kt
          HomeViewModel.kt
          HomeUiState.kt
        profile/
          ProfileScreen.kt
          ProfileViewModel.kt
      components/
        LoadingIndicator.kt
        ErrorMessage.kt
    data/
      local/
        AppDatabase.kt
        UserDao.kt
        UserEntity.kt
      remote/
        ApiService.kt
        RetrofitClient.kt
      repository/
        UserRepository.kt
        UserRepositoryImpl.kt
    domain/
      model/
        User.kt
      usecase/
        GetUserUseCase.kt
  src/test/java/...           # Unit tests
  src/androidTest/java/...    # UI tests
```

### build.gradle.kts (App Level)

```kotlin
plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("com.google.dagger.hilt.android")
    id("com.google.devtools.ksp")
}

android {
    namespace = "com.example.app"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.example.app"
        minSdk = 26
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"
    }

    buildFeatures {
        compose = true
    }

    composeOptions {
        kotlinCompilerExtensionVersion = "1.5.10"
    }

    kotlinOptions {
        jvmTarget = "1.8"
    }
}

dependencies {
    // Compose BOM
    val composeBom = platform("androidx.compose:compose-bom:2024.02.00")
    implementation(composeBom)
    androidTestImplementation(composeBom)

    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.ui:ui-tooling-preview")
    debugImplementation("androidx.compose.ui:ui-tooling")

    // Navigation
    implementation("androidx.navigation:navigation-compose:2.7.7")

    // ViewModel + Lifecycle
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.7.0")
    implementation("androidx.lifecycle:lifecycle-runtime-compose:2.7.0")
    implementation("androidx.activity:activity-compose:1.8.2")

    // Hilt
    implementation("com.google.dagger:hilt-android:2.50")
    ksp("com.google.dagger:hilt-compiler:2.50")
    implementation("androidx.hilt:hilt-navigation-compose:1.1.0")

    // Room
    implementation("androidx.room:room-runtime:2.6.1")
    implementation("androidx.room:room-ktx:2.6.1")
    ksp("androidx.room:room-compiler:2.6.1")

    // Retrofit + OkHttp
    implementation("com.squareup.retrofit2:retrofit:2.9.0")
    implementation("com.squareup.retrofit2:converter-moshi:2.9.0")
    implementation("com.squareup.okhttp3:logging-interceptor:4.12.0")

    // DataStore
    implementation("androidx.datastore:datastore-preferences:1.0.0")

    // Coroutines
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3")

    // Testing
    testImplementation("junit:junit:4.13.2")
    testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.7.3")
    testImplementation("app.cash.turbine:turbine:1.0.0")
    androidTestImplementation("androidx.compose.ui:ui-test-junit4")
    androidTestImplementation("androidx.test.ext:junit:1.1.5")
    debugImplementation("androidx.compose.ui:ui-test-manifest")
}
```

---

## 2. Jetpack Compose

### Composable Structure

```kotlin
@Composable
fun HomeScreen(
    viewModel: HomeViewModel = hiltViewModel(),
    onNavigateToProfile: (String) -> Unit
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    HomeContent(
        uiState = uiState,
        onRefresh = viewModel::refresh,
        onUserClick = onNavigateToProfile
    )
}

@Composable
fun HomeContent(
    uiState: HomeUiState,
    onRefresh: () -> Unit,
    onUserClick: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    when (uiState) {
        is HomeUiState.Loading -> LoadingIndicator()
        is HomeUiState.Success -> UserList(
            users = uiState.users,
            onUserClick = onUserClick
        )
        is HomeUiState.Error -> ErrorMessage(
            message = uiState.message,
            onRetry = onRefresh
        )
    }
}
```

### State Management

```kotlin
@Composable
fun Counter() {
    var count by remember { mutableIntStateOf(0) }

    Button(onClick = { count++ }) {
        Text("Count: $count")
    }
}
```

### Derived State

```kotlin
@Composable
fun SearchableList(items: List<String>, query: String) {
    val filteredItems by remember(query, items) {
        derivedStateOf {
            items.filter { it.contains(query, ignoreCase = true) }
        }
    }

    LazyColumn {
        items(filteredItems) { item ->
            Text(item)
        }
    }
}
```

### Side Effects

```kotlin
@Composable
fun UserProfile(userId: String) {
    val snackbarHostState = remember { SnackbarHostState() }

    LaunchedEffect(userId) {
        // Runs when userId changes; coroutine scope
        viewModel.loadUser(userId)
    }

    DisposableEffect(Unit) {
        // Setup/cleanup pattern
        val listener = object : SomeListener { ... }
        onDispose { listener.cleanup() }
    }

    SideEffect {
        // Runs on every recomposition; use sparingly
        analytics.trackScreen("profile")
    }
}
```

### Material Design 3 Theme

```kotlin
// ui/theme/Theme.kt
@Composable
fun AppTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    val colorScheme = if (darkTheme) DarkColorScheme else LightColorScheme

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}
```

---

## 3. MVVM Architecture

### UiState Pattern

```kotlin
// ui/screens/home/HomeUiState.kt
sealed interface HomeUiState {
    data object Loading : HomeUiState
    data class Success(val users: List<User>) : HomeUiState
    data class Error(val message: String) : HomeUiState
}
```

### ViewModel

```kotlin
// ui/screens/home/HomeViewModel.kt
@HiltViewModel
class HomeViewModel @Inject constructor(
    private val getUsersUseCase: GetUsersUseCase
) : ViewModel() {

    private val _uiState = MutableStateFlow<HomeUiState>(HomeUiState.Loading)
    val uiState: StateFlow<HomeUiState> = _uiState.asStateFlow()

    init {
        loadUsers()
    }

    fun refresh() {
        loadUsers()
    }

    private fun loadUsers() {
        viewModelScope.launch {
            _uiState.value = HomeUiState.Loading
            getUsersUseCase()
                .onSuccess { users ->
                    _uiState.value = HomeUiState.Success(users)
                }
                .onFailure { error ->
                    _uiState.value = HomeUiState.Error(error.message ?: "Unknown error")
                }
        }
    }
}
```

### Repository Pattern

```kotlin
// data/repository/UserRepository.kt
interface UserRepository {
    suspend fun getUsers(): Result<List<User>>
    suspend fun getUser(id: String): Result<User>
}

// data/repository/UserRepositoryImpl.kt
class UserRepositoryImpl @Inject constructor(
    private val apiService: ApiService,
    private val userDao: UserDao
) : UserRepository {

    override suspend fun getUsers(): Result<List<User>> {
        return try {
            val remoteUsers = apiService.getUsers()
            userDao.insertAll(remoteUsers.map { it.toEntity() })
            Result.success(remoteUsers.map { it.toDomain() })
        } catch (e: Exception) {
            // Fallback to local DB
            val localUsers = userDao.getAll().map { it.toDomain() }
            Result.success(localUsers)
        }
    }

    override suspend fun getUser(id: String): Result<User> {
        return try {
            Result.success(apiService.getUser(id).toDomain())
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
```

### UseCase

```kotlin
// domain/usecase/GetUsersUseCase.kt
class GetUsersUseCase @Inject constructor(
    private val userRepository: UserRepository
) {
    suspend operator fun invoke(): Result<List<User>> {
        return userRepository.getUsers()
    }
}
```

---

## 4. Compose Navigation

### Type-Safe Navigation (Compose 1.7+)

```kotlin
// navigation/AppDestinations.kt
@Serializable
object Home

@Serializable
data class Profile(val userId: String)

// navigation/AppNavHost.kt
@Composable
fun AppNavHost(navController: NavHostController) {
    NavHost(navController = navController, startDestination = Home) {
        composable<Home> {
            HomeScreen(
                onNavigateToProfile = { userId ->
                    navController.navigate(Profile(userId))
                }
            )
        }
        composable<Profile> { backStackEntry ->
            val profile: Profile = backStackEntry.toRoute()
            ProfileScreen(userId = profile.userId)
        }
    }
}
```

### Navigation with ViewModel

```kotlin
@Composable
fun ProfileScreen(
    userId: String,
    viewModel: ProfileViewModel = hiltViewModel()
) {
    LaunchedEffect(userId) {
        viewModel.loadUser(userId)
    }
    // ...
}
```

### Bottom Navigation

```kotlin
@Composable
fun BottomNavBar(navController: NavHostController) {
    val items = listOf("home", "search", "profile")
    NavigationBar {
        items.forEach { screen ->
            NavigationBarItem(
                icon = { Icon(...) },
                label = { Text(screen) },
                selected = currentRoute == screen,
                onClick = {
                    navController.navigate(screen) {
                        popUpTo(navController.graph.startDestinationId) { saveState = true }
                        launchSingleTop = true
                        restoreState = true
                    }
                }
            )
        }
    }
}
```

---

## 5. Dependency Injection (Hilt)

### Application Setup

```kotlin
// App.kt
@HiltAndroidApp
class MyApp : Application()
```

### AndroidManifest.xml

```xml
<application
    android:name=".MyApp"
    android:icon="@mipmap/ic_launcher"
    android:theme="@style/Theme.MyApp">
    <activity android:name=".MainActivity" android:exported="true">
        <intent-filter>
            <action android:name="android.intent.action.MAIN" />
            <category android:name="android.intent.category.LAUNCHER" />
        </intent-filter>
    </activity>
</application>
```

### Network Module

```kotlin
// di/NetworkModule.kt
@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {

    @Provides
    @Singleton
    fun provideOkHttpClient(): OkHttpClient {
        return OkHttpClient.Builder()
            .addInterceptor(HttpLoggingInterceptor().apply {
                level = HttpLoggingInterceptor.Level.BODY
            })
            .build()
    }

    @Provides
    @Singleton
    fun provideRetrofit(okHttpClient: OkHttpClient): Retrofit {
        return Retrofit.Builder()
            .baseUrl("https://api.example.com/")
            .client(okHttpClient)
            .addConverterFactory(MoshiConverterFactory.create())
            .build()
    }

    @Provides
    @Singleton
    fun provideApiService(retrofit: Retrofit): ApiService {
        return retrofit.create(ApiService::class.java)
    }
}
```

### Database Module

```kotlin
// di/DatabaseModule.kt
@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {

    @Provides
    @Singleton
    fun provideDatabase(@ApplicationContext context: Context): AppDatabase {
        return Room.databaseBuilder(
            context,
            AppDatabase::class.java,
            "app_database"
        ).build()
    }

    @Provides
    fun provideUserDao(database: AppDatabase): UserDao {
        return database.userDao()
    }
}
```

### Repository Binding

```kotlin
// di/RepositoryModule.kt
@Module
@InstallIn(ViewModelComponent::class)
abstract class RepositoryModule {

    @Binds
    abstract fun bindUserRepository(
        impl: UserRepositoryImpl
    ): UserRepository
}
```

---

## 6. Persistence (Room & DataStore)

### Room Entity and DAO

```kotlin
// data/local/UserEntity.kt
@Entity(tableName = "users")
data class UserEntity(
    @PrimaryKey val id: String,
    val username: String,
    val email: String
)

// data/local/UserDao.kt
@Dao
interface UserDao {
    @Query("SELECT * FROM users")
    suspend fun getAll(): List<UserEntity>

    @Query("SELECT * FROM users WHERE id = :id")
    suspend fun getById(id: String): UserEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(users: List<UserEntity>)

    @Delete
    suspend fun delete(user: UserEntity)
}

// data/local/AppDatabase.kt
@Database(entities = [UserEntity::class], version = 1)
abstract class AppDatabase : RoomDatabase() {
    abstract fun userDao(): UserDao
}
```

### DataStore Preferences

```kotlin
// data/local/SettingsDataStore.kt
class SettingsDataStore @Inject constructor(
    @ApplicationContext private val context: Context
) {
    private val dataStore = context.dataStore

    val isDarkMode = dataStore.data
        .map { preferences -> preferences[DARK_MODE_KEY] ?: false }

    suspend fun setDarkMode(enabled: Boolean) {
        dataStore.edit { preferences ->
            preferences[DARK_MODE_KEY] = enabled
        }
    }

    companion object {
        private val DARK_MODE_KEY = booleanPreferencesKey("dark_mode")
    }
}
```

---

## 7. Networking (Retrofit & OkHttp)

### API Service

```kotlin
// data/remote/ApiService.kt
interface ApiService {
    @GET("users")
    suspend fun getUsers(): List<UserDto>

    @GET("users/{id}")
    suspend fun getUser(@Path("id") id: String): UserDto

    @POST("users")
    suspend fun createUser(@Body user: UserDto): UserDto
}
```

### DTO to Domain Mapper

```kotlin
// data/remote/UserDto.kt
data class UserDto(
    val id: String,
    val username: String,
    val email: String
)

fun UserDto.toDomain(): User = User(id, username, email)
fun UserDto.toEntity(): UserEntity = UserEntity(id, username, email)
```

### Interceptors

```kotlin
class AuthInterceptor @Inject constructor(
    private val tokenProvider: TokenProvider
) : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val request = chain.request().newBuilder()
            .addHeader("Authorization", "Bearer ${tokenProvider.getToken()}")
            .build()
        return chain.proceed(request)
    }
}
```

---

## 8. Testing

### Unit Test for ViewModel

```kotlin
// test/HomeViewModelTest.kt
class HomeViewModelTest {

    private val getUsersUseCase = mockk<GetUsersUseCase>()
    private lateinit var viewModel: HomeViewModel

    @Before
    fun setup() {
        Dispatchers.setMain(StandardTestDispatcher())
        viewModel = HomeViewModel(getUsersUseCase)
    }

    @After
    fun tearDown() {
        Dispatchers.resetMain()
    }

    @Test
    fun `load users emits success state`() = runTest {
        val users = listOf(User("1", "John", "john@test.com"))
        coEvery { getUsersUseCase() } returns Result.success(users)

        viewModel.uiState.test {
            assertEquals(HomeUiState.Loading, awaitItem())
            assertEquals(HomeUiState.Success(users), awaitItem())
            cancelAndIgnoreRemainingEvents()
        }
    }
}
```

### Compose UI Test

```kotlin
// androidTest/HomeScreenTest.kt
class HomeScreenTest {

    @get:Rule
    val composeTestRule = createComposeRule()

    @Test
    fun userList_displaysUsers() {
        val users = listOf(User("1", "John", "john@test.com"))

        composeTestRule.setContent {
            AppTheme {
                HomeContent(
                    uiState = HomeUiState.Success(users),
                    onRefresh = {},
                    onUserClick = {}
                )
            }
        }

        composeTestRule.onNodeWithText("John").assertIsDisplayed()
    }

    @Test
    fun error_showsRetryButton() {
        composeTestRule.setContent {
            AppTheme {
                HomeContent(
                    uiState = HomeUiState.Error("Network error"),
                    onRefresh = {},
                    onUserClick = {}
                )
            }
        }

        composeTestRule.onNodeWithText("Retry").assertIsDisplayed()
        composeTestRule.onNodeWithText("Retry").performClick()
    }
}
```

### Repository Test

```kotlin
class UserRepositoryTest {

    private val apiService = mockk<ApiService>()
    private val userDao = mockk<UserDao>()
    private val repository = UserRepositoryImpl(apiService, userDao)

    @Test
    fun `getUsers returns remote data on success`() = runTest {
        val dtoUsers = listOf(UserDto("1", "John", "john@test.com"))
        coEvery { apiService.getUsers() } returns dtoUsers
        coEvery { userDao.insertAll(any()) } just Runs

        val result = repository.getUsers()

        assertTrue(result.isSuccess)
        assertEquals(1, result.getOrNull()?.size)
    }
}
```

---

## 9. Best Practices Checklist

- [ ] Application Factory pattern: `@HiltAndroidApp` in `Application` class
- [ ] Compose state is unidirectional: ViewModel â†’ StateFlow â†’ Composable
- [ ] `collectAsStateWithLifecycle()` used instead of `collectAsState()`
- [ ] UI state represented as sealed interface (`Loading`, `Success`, `Error`)
- [ ] Repository pattern with local/remote data sources
- [ ] UseCases encapsulate single business logic operations
- [ ] Hilt modules are organized by layer (`NetworkModule`, `DatabaseModule`)
- [ ] Room entities use `data class` with `@Entity` and `@PrimaryKey`
- [ ] Retrofit DTOs mapped to domain models; domain models used in UI
- [ ] `Result<T>` type used for error handling across layers
- [ ] Compose previews exist for every screen composable
- [ ] Tests use `StandardTestDispatcher` and `runTest` for coroutines
- [ ] Compose UI tests use semantic matchers (`onNodeWithText`, `onNodeWithTag`)
- [ ] Navigation uses type-safe routes (not string-based)
- [ ] Deep links configured for key screens
- [ ] Material Design 3 theming applied consistently
- [ ] Dark mode support via `isSystemInDarkTheme()`
- [ ] `Modifier` parameter exposed on every reusable component
- [ ] `derivedStateOf` used for expensive computations in Compose
- [ ] `LaunchedEffect` keys are specific (not `Unit` unless truly once)

---

## 10. Common Pitfalls

| Problem | Cause | Solution |
|---------|-------|----------|
| Infinite recomposition | State read inside `SideEffect` without key | Use `LaunchedEffect` or `derivedStateOf` |
| Memory leak in ViewModel | `viewModelScope` used for long-running ops | Use `lifecycleScope` in Activity/Fragment |
| Room crash on schema change | Version mismatch without migration | Increment version or use `fallbackToDestructiveMigration()` |
| Hilt "cannot be provided" | Missing `@Provides` or `@Binds` | Check module bindings and `@InstallIn` scope |
| Navigation state lost | No `saveState` / `restoreState` | Add `popUpTo { saveState = true }` + `restoreState = true` |
| Compose preview fails | Hilt or context dependency in composable | Use `@PreviewParameter` or mock data |
| `collectAsState` in background | Not lifecycle-aware | Use `collectAsStateWithLifecycle()` |
| Network on main thread | Retrofit without coroutines adapter | Use `suspend` functions in Retrofit interface |
| Double API call | `LaunchedEffect(Unit)` in recomposition | Use specific keys or `remember` for stable references |
| Test hangs | Missing `StandardTestDispatcher` | Call `Dispatchers.setMain(dispatcher)` in `@Before` |

---

## 11. References

- [Android Developers â€” Jetpack Compose](https://developer.android.com/jetpack/compose)
- [Material Design 3 â€” Compose](https://developer.android.com/reference/kotlin/androidx/compose/material3/package-summary)
- [Hilt Documentation](https://example.com/android-hilt)
- [Room Documentation](https://developer.android.com/training/data-storage/room)
- [Retrofit](https://square.github.io/retrofit/)
- [Compose Navigation](https://developer.android.com/jetpack/compose/navigation)
- [Kotlin Coroutines on Android](https://developer.android.com/kotlin/coroutines)
- Related skills: `mobile-android-design`, `kotlin-patterns`, `kotlin-springboot`
