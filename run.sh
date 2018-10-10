# kernprof -l main.py \

max-iter() {
	if [ $1 -le 4 ]; then
		echo 20
	elif [ $1 -le 8 ]; then
		echo 125
	else
		echo 200
	fi
}

for meth in swap; do
	for instance in {9..12}; do
		for seed in {0..4}; do
			echo WTA$instance $seed
			python main.py \
				--instance-file data/WTA$instance \
				--population-size $[instance*250] \
				--max-iterations $(max-iter $instance) \
				--tournament-size 0.05 \
				--selection-probability 0.5 \
				--selection-size 0.2 \
				--mutation-probability 0.5 \
				--seed $seed \
				--mutation-method $meth > /dev/null
		done
	done
done
