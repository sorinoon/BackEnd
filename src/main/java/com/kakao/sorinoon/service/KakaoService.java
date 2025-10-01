package com.kakao.sorinoon.service;

import com.kakao.sorinoon.dto.KakaoTokenResponseDto;
import com.kakao.sorinoon.dto.KakaoUserInfoResponseDto;
import io.netty.handler.codec.http.HttpHeaderValues;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatusCode;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

import java.util.Objects;


@Slf4j
@Service
public class KakaoService {

    private final String clientId;
    private final String redirectUri;
    private final String KAUTH_TOKEN_URL_HOST;
    private final String KAUTH_USER_URL_HOST;

    @Autowired
    public KakaoService(@Value("${kakao.client_id}") String clientId,
                        @Value("${kakao.redirect_uri}") String redirectUri) {
        this.clientId = clientId;
        this.redirectUri = redirectUri;
        this.KAUTH_TOKEN_URL_HOST = "https://kauth.kakao.com";
        this.KAUTH_USER_URL_HOST = "https://kapi.kakao.com";
    }

    public Mono<String> getAccessTokenFromKakao(String code) {
        return WebClient.create(KAUTH_TOKEN_URL_HOST).post()
                .uri(uriBuilder -> uriBuilder
                        .scheme("https")
                        .path("/oauth/token")
                        .queryParam("grant_type", "authorization_code")
                        .queryParam("client_id", clientId)
                        .queryParam("redirect_uri", redirectUri)
                        .queryParam("code", code)
                        .build(true))
                .header(HttpHeaders.CONTENT_TYPE, HttpHeaderValues.APPLICATION_X_WWW_FORM_URLENCODED.toString())
                .retrieve()
                .onStatus(HttpStatusCode::is4xxClientError, clientResponse -> Mono.error(new RuntimeException("Invalid Parameter")))
                .onStatus(HttpStatusCode::is5xxServerError, clientResponse -> Mono.error(new RuntimeException("Internal Server Error")))
                .bodyToMono(KakaoTokenResponseDto.class)
                .doOnNext(kakaoTokenResponseDto -> {
                    log.info(" [Kakao Service] Access Token ------> {}", Objects.requireNonNull(kakaoTokenResponseDto).getAccessToken());
                    log.info(" [Kakao Service] Refresh Token ------> {}", kakaoTokenResponseDto.getRefreshToken());
                    log.info(" [Kakao Service] Id Token ------> {}", kakaoTokenResponseDto.getIdToken());
                    log.info(" [Kakao Service] Scope ------> {}", kakaoTokenResponseDto.getScope());
                })
                .map(KakaoTokenResponseDto::getAccessToken);
    }





    public Mono<KakaoUserInfoResponseDto> getUserInfo(String accessToken) {
        return WebClient.create(KAUTH_USER_URL_HOST)
                .get()
                .uri(uriBuilder -> uriBuilder
                        .scheme("https")
                        .path("/v2/user/me")
                        .build(true))
                .header(HttpHeaders.AUTHORIZATION, "Bearer " + accessToken)
                .header(HttpHeaders.CONTENT_TYPE, HttpHeaderValues.APPLICATION_X_WWW_FORM_URLENCODED.toString())
                .retrieve()
                .onStatus(HttpStatusCode::is4xxClientError, clientResponse -> Mono.error(new RuntimeException("Invalid Parameter")))
                .onStatus(HttpStatusCode::is5xxServerError, clientResponse -> Mono.error(new RuntimeException("Internal Server Error")))
                .bodyToMono(KakaoUserInfoResponseDto.class)
                .doOnNext(userInfo -> {
                    log.info("[ Kakao Service ] Auth ID ---> {} ", userInfo.getId());
                    log.info("[ Kakao Service ] NickName ---> {} ", userInfo.getKakaoAccount().getProfile().getNickName());
                    log.info("[ Kakao Service ] ProfileImageUrl ---> {} ", userInfo.getKakaoAccount().getProfile().getProfileImageUrl());
                });
    }
}