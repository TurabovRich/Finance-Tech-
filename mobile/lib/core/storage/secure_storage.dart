import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

const _tokenKey = 'access_token';

final secureStorageProvider = Provider<SecureTokenStorage>((ref) {
  return SecureTokenStorage(const FlutterSecureStorage());
});

class SecureTokenStorage {
  SecureTokenStorage(this._storage);

  final FlutterSecureStorage _storage;

  Future<void> saveToken(String token) => _storage.write(key: _tokenKey, value: token);

  Future<String?> readToken() => _storage.read(key: _tokenKey);

  Future<void> clear() => _storage.delete(key: _tokenKey);
}
