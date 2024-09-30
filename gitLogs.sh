for d in /path/to/BaseDIR/*/.git; do
    r=${d%.git}
    echo "$r"
    repo_name=$(basename "$r")
    git -C "$r" log \
        --committer=<yourEmailid@domain.in> \
        --after=$1 \
        --before=$2 \
        --reverse \
        --numstat \
        --pretty='format:--%h--%cd--%s' |
    awk -v repo_name="$repo_name" '
        function print_commit() {
            if(commit_hash != "") {
                print repo_name, commit_hash, commit_date, commit_subject, plus, minus;
                commit_hash = ""; commit_date = ""; commit_subject = "";
                plus = 0; minus = 0;
            }
        }
        /^--/ {
            print_commit();
            split($0, arr, "--");
            commit_hash = arr[2];
            commit_date = arr[3];
            commit_subject = arr[4];
        }
        /^[0-9]/ {
            split($0, stats, "\t");
            plus += stats[1];
            minus += stats[2];
        }
        END {
            print_commit();
        }
    '
done

