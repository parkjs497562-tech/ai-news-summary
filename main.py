import argparse

from src.database import (
    get_unsummarized_news,
    get_news_by_id,
    save_summary
)

from src.summarizer import summarize_text


def summarize_news(news_list):
    """
    뉴스 목록을 받아 AI 요약을 실행하고
    결과를 데이터베이스에 저장한다.
    """

    total = len(news_list)
    success_count = 0
    fail_count = 0

    print(f"[INFO] 요약 대상: {total}건")

    for index, (news_id, title, content) in enumerate(
        news_list,
        start=1
    ):

        print(
            f"[INFO] [{index}/{total}] "
            f"ID={news_id} 요약 시작"
        )

        # OpenAI API로 요약
        summary = summarize_text(content)

        # 요약 성공
        if summary:

            save_summary(news_id, summary)

            print(
                f"[INFO] [{index}/{total}] "
                f"ID={news_id} 요약 완료 "
                f"({len(content)}자 → {len(summary)}자)"
            )

            success_count += 1

        # 요약 실패
        else:

            print(
                f"[INFO] [{index}/{total}] "
                f"ID={news_id} 요약 실패"
            )

            fail_count += 1

    print(
        f"[INFO] 요약 완료: "
        f"{success_count}건 성공, "
        f"{fail_count}건 실패"
    )


def main():

    # CLI 기본 설정
    parser = argparse.ArgumentParser(
        description="AI 뉴스 요약 프로그램"
    )

    subparsers = parser.add_subparsers(
        dest="command"
    )


    # =========================
    # summarize 명령어
    # =========================

    summarize_parser = subparsers.add_parser(
        "summarize",
        help="뉴스를 AI로 요약합니다."
    )


    # --all
    summarize_parser.add_argument(
        "--all",
        action="store_true",
        help="요약되지 않은 모든 뉴스를 요약합니다."
    )


    # --unsummarized
    summarize_parser.add_argument(
        "--unsummarized",
        action="store_true",
        help="아직 요약되지 않은 뉴스만 요약합니다."
    )


    # --limit
    summarize_parser.add_argument(
        "--limit",
        type=int,
        help="요약할 뉴스의 최대 개수입니다."
    )


    # --id
    summarize_parser.add_argument(
        "--id",
        type=int,
        help="특정 뉴스 ID를 요약합니다."
    )


    args = parser.parse_args()


    # =========================
    # summarize 실행
    # =========================

    if args.command == "summarize":

        # -------------------------
        # 특정 뉴스 ID
        # -------------------------

        if args.id is not None:

            news = get_news_by_id(args.id)

            if not news:

                print(
                    f"[ERROR] ID={args.id}인 "
                    f"뉴스를 찾을 수 없습니다."
                )

                return


            news_id, title, content, summary = news


            # 이미 요약된 뉴스
            if summary:

                print(
                    f"[INFO] ID={news_id}는 "
                    f"이미 요약되어 있습니다."
                )

                return


            # AI 요약 실행
            summarize_news([
                (news_id, title, content)
            ])


        # -------------------------
        # --all
        # -------------------------

        elif args.all:

            news_list = get_unsummarized_news()

            if args.limit is not None:
                news_list = news_list[:args.limit]

            summarize_news(news_list)


        # -------------------------
        # --unsummarized
        # -------------------------

        elif args.unsummarized:

            news_list = get_unsummarized_news()

            if args.limit is not None:
                news_list = news_list[:args.limit]

            summarize_news(news_list)


        # -------------------------
        # 옵션이 없는 경우
        # -------------------------

        else:

            print(
                "[INFO] 옵션이 없으므로 "
                "미요약 뉴스만 요약합니다."
            )

            news_list = get_unsummarized_news()

            if args.limit is not None:
                news_list = news_list[:args.limit]

            summarize_news(news_list)


    else:

        parser.print_help()


if __name__ == "__main__":
    main()



