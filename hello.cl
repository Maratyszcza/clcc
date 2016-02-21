kernel void f0(global uint dest[])
{
	dest[0] = 0;
}

kernel void f_local_id(global uint dest[])
{
	const size_t i = get_local_id(0);
	dest[i] = i;
}

kernel void f_global_id(global uint dest[])
{
	const size_t i = get_global_id(0);
	dest[i] = i;
}

kernel void g0(global uint dest[], global const uint src[]) {
	dest[0] = src[0];
}

kernel __attribute__((reqd_work_group_size(256, 1, 1))) void f0_group256(global uint dest[]) {
	dest[0] = 0;
}

kernel __attribute__((reqd_work_group_size(192, 1, 1))) void f0_group192(global uint dest[]) {
	dest[0] = 0;
}

kernel __attribute__((reqd_work_group_size(128, 1, 1))) void f0_group128(global uint dest[]) {
	dest[0] = 0;
}

kernel __attribute__((reqd_work_group_size(64, 1, 1))) void f0_group64(global uint dest[]) {
	dest[0] = 0;
}

