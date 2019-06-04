sigint() {
    echo "Exit Shell"
    exit 0
}
trap sigint INT

python3 reactive.py init
while true
do
  python3 reactive.py
done
